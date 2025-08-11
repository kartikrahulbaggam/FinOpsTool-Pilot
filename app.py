from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pyodbc
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database connection configuration
DB_SERVER = os.getenv('DB_SERVER', 'your-server.database.windows.net')
DB_NAME = os.getenv('DB_NAME', 'your-database-name')
DB_USERNAME = os.getenv('DB_USERNAME', 'your-username')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your-password')
DB_DRIVER = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')

def get_db_connection():
    """Create and return database connection"""
    try:
        conn_str = f"DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USERNAME};PWD={DB_PASSWORD}"
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/cost-analysis', methods=['POST'])
def get_cost_analysis():
    """Get cost analysis based on month, year, and filters"""
    try:
        data = request.get_json()
        month = data.get('month')
        year = data.get('year')
        client_filter = data.get('client', '')
        product_group_filter = data.get('productGroup', '')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        # Build the SQL query based on filters
        query = """
        SELECT 
            ClientName,
            ProductGroup,
            SUM(Cost) as TotalCost,
            COUNT(*) as TransactionCount
        FROM CostData 
        WHERE MONTH(TransactionDate) = ? 
        AND YEAR(TransactionDate) = ?
        """
        
        params = [month, year]
        
        if client_filter:
            query += " AND ClientName LIKE ?"
            params.append(f'%{client_filter}%')
        
        if product_group_filter:
            query += " AND ProductGroup LIKE ?"
            params.append(f'%{product_group_filter}%')
        
        query += " GROUP BY ClientName, ProductGroup ORDER BY TotalCost DESC"
        
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        
        return jsonify({
            'success': True,
            'data': df.to_dict('records'),
            'totalCost': float(df['TotalCost'].sum()),
            'totalTransactions': int(df['TransactionCount'].sum())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-clients', methods=['GET'])
def get_top_clients():
    """Get top 10 clients by cost"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        query = """
        SELECT TOP 10
            ClientName,
            SUM(Cost) as TotalCost,
            COUNT(*) as TransactionCount
        FROM CostData 
        GROUP BY ClientName 
        ORDER BY TotalCost DESC
        """
        
        df = pd.read_sql(query, conn)
        conn.close()
        
        return jsonify({
            'success': True,
            'data': df.to_dict('records')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/product-groups', methods=['GET'])
def get_product_groups():
    """Get all product groups"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        query = "SELECT DISTINCT ProductGroup FROM CostData ORDER BY ProductGroup"
        df = pd.read_sql(query, conn)
        conn.close()
        
        return jsonify({
            'success': True,
            'data': df['ProductGroup'].tolist()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clients', methods=['GET'])
def get_clients():
    """Get all clients"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        query = "SELECT DISTINCT ClientName FROM CostData ORDER BY ClientName"
        df = pd.read_sql(query, conn)
        conn.close()
        
        return jsonify({
            'success': True,
            'data': df['ClientName'].tolist()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)