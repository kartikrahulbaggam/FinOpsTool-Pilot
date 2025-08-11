// Main Application JavaScript
class CostAnalysisApp {
    constructor() {
        this.initializeApp();
        this.bindEvents();
        this.loadInitialData();
    }

    initializeApp() {
        // Populate year dropdown with current year and previous 5 years
        const currentYear = new Date().getFullYear();
        const yearSelect = document.getElementById('year');
        
        for (let year = currentYear; year >= currentYear - 5; year--) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearSelect.appendChild(option);
        }

        // Set current month and year as default
        const currentMonth = new Date().getMonth() + 1;
        document.getElementById('month').value = currentMonth;
        document.getElementById('year').value = currentYear;
    }

    bindEvents() {
        // Analyze button click
        document.getElementById('analyzeBtn').addEventListener('click', () => {
            this.performCostAnalysis();
        });

        // Top clients button click
        document.getElementById('topClientsBtn').addEventListener('click', () => {
            this.toggleTopClients();
        });

        // Product analysis button click
        document.getElementById('productAnalysisBtn').addEventListener('click', () => {
            this.toggleProductAnalysis();
        });

        // Smooth scrolling for navigation links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    async loadInitialData() {
        try {
            this.showLoading();
            
            // Load clients and product groups
            const [clientsResponse, productGroupsResponse] = await Promise.all([
                fetch('/api/clients'),
                fetch('/api/product-groups')
            ]);

            if (clientsResponse.ok && productGroupsResponse.ok) {
                const clients = await clientsResponse.json();
                const productGroups = await productGroupsResponse.json();

                this.populateDropdown('client', clients.data);
                this.populateDropdown('productGroup', productGroups.data);
                
                // Update dashboard stats
                this.updateDashboardStats(clients.data.length, productGroups.data.length);
            }

            // Load top clients for initial display
            await this.loadTopClients();
            
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showError('Failed to load initial data');
        } finally {
            this.hideLoading();
        }
    }

    populateDropdown(selectId, data) {
        const select = document.getElementById(selectId);
        const currentValue = select.value;
        
        // Clear existing options except the first one
        while (select.children.length > 1) {
            select.removeChild(select.lastChild);
        }

        // Add new options
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item;
            option.textContent = item;
            select.appendChild(option);
        });

        // Restore previous selection if it still exists
        if (currentValue && data.includes(currentValue)) {
            select.value = currentValue;
        }
    }

    updateDashboardStats(clientCount, productCount) {
        document.getElementById('totalClients').textContent = clientCount;
        document.getElementById('totalProducts').textContent = productCount;
    }

    async performCostAnalysis() {
        const month = document.getElementById('month').value;
        const year = document.getElementById('year').value;
        const client = document.getElementById('client').value;
        const productGroup = document.getElementById('productGroup').value;

        if (!month || !year) {
            this.showError('Please select both month and year');
            return;
        }

        try {
            this.showLoading();

            const response = await fetch('/api/cost-analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    month: parseInt(month),
                    year: parseInt(year),
                    client: client,
                    productGroup: productGroup
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.displayCostAnalysisResults(data);
            } else {
                const errorData = await response.json();
                this.showError(errorData.error || 'Analysis failed');
            }

        } catch (error) {
            console.error('Error performing cost analysis:', error);
            this.showError('Failed to perform cost analysis');
        } finally {
            this.hideLoading();
        }
    }

    displayCostAnalysisResults(data) {
        // Update summary cards
        document.getElementById('analysisTotalCost').textContent = this.formatCurrency(data.totalCost);
        document.getElementById('analysisTransactions').textContent = data.totalTransactions.toLocaleString();

        // Update results table
        const tableBody = document.getElementById('resultsTableBody');
        tableBody.innerHTML = '';

        if (data.data && data.data.length > 0) {
            data.data.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${row.ClientName}</td>
                    <td>${row.ProductGroup}</td>
                    <td>${this.formatCurrency(row.TotalCost)}</td>
                    <td>${row.TransactionCount.toLocaleString()}</td>
                `;
                tableBody.appendChild(tr);
            });
        } else {
            const tr = document.createElement('tr');
            tr.innerHTML = '<td colspan="4" style="text-align: center; padding: 2rem;">No data found for the selected criteria</td>';
            tableBody.appendChild(tr);
        }

        // Scroll to results
        document.getElementById('analysis').scrollIntoView({ behavior: 'smooth' });
    }

    async loadTopClients() {
        try {
            const response = await fetch('/api/top-clients');
            if (response.ok) {
                const data = await response.json();
                this.displayTopClients(data.data);
            }
        } catch (error) {
            console.error('Error loading top clients:', error);
        }
    }

    displayTopClients(clients) {
        const content = document.getElementById('topClientsContent');
        
        if (clients && clients.length > 0) {
            let html = '<div class="top-clients-list">';
            clients.forEach((client, index) => {
                html += `
                    <div class="client-item">
                        <span class="rank">${index + 1}</span>
                        <span class="client-name">${client.ClientName}</span>
                        <span class="client-cost">${this.formatCurrency(client.TotalCost)}</span>
                    </div>
                `;
            });
            html += '</div>';
            content.innerHTML = html;
        } else {
            content.innerHTML = '<p>No client data available</p>';
        }
    }

    toggleTopClients() {
        const content = document.getElementById('topClientsContent');
        const button = document.getElementById('topClientsBtn');
        
        if (content.classList.contains('hidden')) {
            content.classList.remove('hidden');
            button.innerHTML = '<i class="fas fa-eye-slash"></i> Hide Top Clients';
        } else {
            content.classList.add('hidden');
            button.innerHTML = '<i class="fas fa-trophy"></i> View Top Clients';
        }
    }

    toggleProductAnalysis() {
        const content = document.getElementById('productAnalysisContent');
        const button = document.getElementById('productAnalysisBtn');
        
        if (content.classList.contains('hidden')) {
            content.classList.remove('hidden');
            button.innerHTML = '<i class="fas fa-eye-slash"></i> Hide Analysis';
            this.loadProductAnalysis();
        } else {
            content.classList.add('hidden');
            button.innerHTML = '<i class="fas fa-chart-pie"></i> View Analysis';
        }
    }

    async loadProductAnalysis() {
        // This would be implemented in Phase 2
        const content = document.getElementById('productAnalysisContent');
        content.innerHTML = '<p>Product Group Analysis will be available in Phase 2</p>';
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        }).format(amount);
    }

    showLoading() {
        document.getElementById('loadingOverlay').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }

    showError(message) {
        // Create a simple error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-notification';
        errorDiv.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: #e53e3e;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            z-index: 3000;
            max-width: 300px;
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CostAnalysisApp();
});

// Add smooth scrolling behavior for all internal links
document.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth' });
        }
    }
});