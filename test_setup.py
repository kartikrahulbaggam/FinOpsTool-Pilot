#!/usr/bin/env python3
"""
Test script to validate the Cost Analysis Dashboard setup
Run this script to test database connectivity and basic functionality
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test if environment variables are properly set"""
    print("🔍 Testing environment configuration...")
    
    load_dotenv()
    
    required_vars = ['DB_SERVER', 'DB_NAME', 'DB_USERNAME', 'DB_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please copy .env.example to .env and fill in your database credentials")
        return False
    else:
        print("✅ Environment variables configured")
        return True

def test_dependencies():
    """Test if required Python packages are installed"""
    print("\n🔍 Testing Python dependencies...")
    
    required_packages = [
        'flask', 'flask_cors', 'pyodbc', 'pandas', 
        'numpy', 'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def test_database_connection():
    """Test database connectivity"""
    print("\n🔍 Testing database connection...")
    
    try:
        import pyodbc
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Build connection string
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USERNAME')};"
            f"PWD={os.getenv('DB_PASSWORD')}"
        )
        
        # Test connection
        conn = pyodbc.connect(conn_str)
        print("✅ Database connection successful")
        
        # Test basic query
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()
        print(f"✅ Database version: {version[0][:50]}...")
        
        # Test if CostData table exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'CostData'
        """)
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("✅ CostData table found")
            
            # Test sample query
            cursor.execute("SELECT TOP 1 ClientName, ProductGroup, Cost FROM CostData")
            sample_data = cursor.fetchone()
            if sample_data:
                print(f"✅ Sample data found: {sample_data[0]} - {sample_data[1]} - ${sample_data[2]}")
            else:
                print("⚠️  CostData table exists but is empty")
        else:
            print("❌ CostData table not found")
            print("Please create the table using the schema in README.md")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Verify your database credentials in .env file")
        print("2. Ensure Azure SQL Database is accessible")
        print("3. Check firewall rules and network access")
        print("4. Verify ODBC Driver 17 is installed")
        return False

def test_flask_app():
    """Test if Flask app can start"""
    print("\n🔍 Testing Flask application...")
    
    try:
        # Import app
        from app import app
        
        # Test if app can be created
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Flask application loads successfully")
                return True
            else:
                print(f"❌ Flask application returned status code: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Flask application test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Cost Analysis Dashboard - Setup Validation")
    print("=" * 50)
    
    tests = [
        ("Environment Configuration", test_environment),
        ("Python Dependencies", test_dependencies),
        ("Database Connection", test_database_connection),
        ("Flask Application", test_flask_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("You can now run: python app.py")
        print("Then open http://localhost:5000 in your browser")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before proceeding.")
        print("Check the README.md file for detailed setup instructions.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)