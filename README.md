# Leadership Cost Analysis Dashboard

A professional web application for leadership to analyze costs by month, year, client, and product group. Built with Python Flask backend and modern HTML/CSS/JavaScript frontend.

## Features

### Phase 1 (Current)
- ✅ Month/Year selection for cost analysis
- ✅ Client and Product Group filtering
- ✅ Top 10 Clients by cost
- ✅ Professional, responsive UI with smooth scrolling
- ✅ Real-time data from Azure SQL Database
- ✅ Interactive dashboard with summary statistics

### Phase 2 (Future)
- 🔄 Azure Key Vault integration for secure credential management
- 🔄 Enhanced product group analysis
- 🔄 Additional reporting and visualization features

## Architecture

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python Flask
- **Database**: Azure SQL Database
- **Deployment**: Azure Web App (single service hosting both frontend and backend)

## Prerequisites

### Local Development
- Python 3.8+
- pip (Python package manager)
- ODBC Driver 17 for SQL Server
- Azure SQL Database access

### Azure Deployment
- Azure subscription
- Azure SQL Database
- Azure Web App service
- Azure Key Vault (Phase 2)

## Installation & Setup

### 1. Clone and Setup Project

```bash
# Clone the repository
git clone <your-repo-url>
cd cost-analysis-dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

#### Option A: Direct Connection (Phase 1)
1. Copy `.env.example` to `.env`
2. Update the database credentials in `.env`:

```env
DB_SERVER=your-server.database.windows.net
DB_NAME=your-database-name
DB_USERNAME=your-username
DB_PASSWORD=your-password
DB_DRIVER={ODBC Driver 17 for SQL Server}
```

#### Option B: Azure Key Vault (Phase 2)
1. Set up Azure Key Vault
2. Store database credentials as secrets
3. Update `.env` with Azure Key Vault configuration
4. Modify `app.py` to use Key Vault authentication

### 3. Database Schema

Ensure your Azure SQL Database has a table structure similar to:

```sql
CREATE TABLE CostData (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ClientName NVARCHAR(255) NOT NULL,
    ProductGroup NVARCHAR(255) NOT NULL,
    Cost DECIMAL(18,2) NOT NULL,
    TransactionDate DATE NOT NULL,
    -- Add other relevant fields as needed
);

-- Create indexes for better performance
CREATE INDEX IX_CostData_TransactionDate ON CostData(TransactionDate);
CREATE INDEX IX_CostData_ClientName ON CostData(ClientName);
CREATE INDEX IX_CostData_ProductGroup ON CostData(ProductGroup);
```

## Local Development & Testing

### 1. Start the Application

```bash
# Make sure virtual environment is activated
python app.py
```

The application will start on `http://localhost:5000`

### 2. Test the Application

1. **Open your browser** and navigate to `http://localhost:5000`
2. **Verify the dashboard loads** with summary statistics
3. **Test the cost analysis**:
   - Select a month and year
   - Optionally filter by client or product group
   - Click "Analyze" button
   - Verify results display correctly
4. **Test the Top 10 Clients** feature
5. **Test smooth scrolling** navigation

### 3. Debugging

- Check the browser console for JavaScript errors
- Check the terminal for Python/Flask errors
- Verify database connectivity
- Check environment variables are loaded correctly

## Deployment to Azure

### 1. Prepare for Deployment

```bash
# Create deployment package
pip freeze > requirements.txt

# Test production build locally
export FLASK_ENV=production
python app.py
```

### 2. Azure Web App Deployment

#### Option A: Azure CLI
```bash
# Login to Azure
az login

# Create resource group (if not exists)
az group create --name cost-analysis-rg --location eastus

# Create App Service plan
az appservice plan create --name cost-analysis-plan --resource-group cost-analysis-rg --sku B1

# Create Web App
az webapp create --name cost-analysis-app --resource-group cost-analysis-rg --plan cost-analysis-plan --runtime "PYTHON|3.9"

# Deploy from local directory
az webapp up --name cost-analysis-app --resource-group cost-analysis-rg
```

#### Option B: Azure Portal
1. Go to Azure Portal
2. Create new Web App
3. Choose Python 3.9 runtime
4. Deploy using GitHub Actions or local Git

### 3. Environment Configuration in Azure

1. Go to your Web App in Azure Portal
2. Navigate to **Configuration** → **Application settings**
3. Add the following environment variables:
   - `DB_SERVER`
   - `DB_NAME`
   - `DB_USERNAME`
   - `DB_PASSWORD`
   - `DB_DRIVER`

### 4. Database Access

Ensure your Azure SQL Database:
- Allows connections from Azure services
- Has firewall rules configured for your Web App
- Has the correct user permissions

## Security Considerations

### Phase 1
- Database credentials stored in environment variables
- Basic input validation and SQL injection prevention
- HTTPS enforced in production

### Phase 2 (Enhanced Security)
- Azure Key Vault for credential management
- Managed Identity for Azure services
- Enhanced authentication and authorization
- Audit logging

## Performance Optimization

### Database
- Proper indexing on frequently queried columns
- Query optimization for large datasets
- Connection pooling

### Application
- Caching for frequently accessed data
- Pagination for large result sets
- Async processing for heavy operations

## Monitoring and Maintenance

### Azure Application Insights
- Enable Application Insights for monitoring
- Track performance metrics
- Monitor errors and exceptions

### Logging
- Structured logging for debugging
- Performance monitoring
- User activity tracking

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify connection string
   - Check firewall rules
   - Verify credentials

2. **Application Won't Start**
   - Check Python version compatibility
   - Verify all dependencies installed
   - Check environment variables

3. **Frontend Not Loading**
   - Verify static files are in correct directories
   - Check browser console for errors
   - Verify Flask routes are working

### Debug Mode

For local development, enable debug mode in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## Future Enhancements (Phase 2)

- [ ] Azure Key Vault integration
- [ ] Advanced product group analytics
- [ ] Interactive charts and graphs
- [ ] Export functionality (PDF, Excel)
- [ ] User authentication and role-based access
- [ ] Scheduled reports and notifications
- [ ] Mobile-responsive optimizations
- [ ] Multi-tenant support

## Support

For technical support or questions:
1. Check the troubleshooting section
2. Review Azure documentation
3. Check Flask and Python documentation
4. Review browser console and server logs

## License

This project is proprietary and confidential. All rights reserved.