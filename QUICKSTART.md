# 🚀 Quick Start Guide - Cost Analysis Dashboard

Get your dashboard running in 5 minutes!

## ⚡ Immediate Setup

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# OR (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Database
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Azure SQL Database credentials
nano .env  # or use any text editor
```

**Required .env variables:**
```env
DB_SERVER=your-server.database.windows.net
DB_NAME=your-database-name
DB_USERNAME=your-username
DB_PASSWORD=your-password
DB_DRIVER={ODBC Driver 17 for SQL Server}
```

### 3. Test Setup
```bash
# Run validation tests
python test_setup.py
```

### 4. Start Application
```bash
python app.py
```

### 5. Open Browser
Navigate to: **http://localhost:5000**

## 🧪 Test Your Setup

1. **Dashboard Loads** ✅ - You should see the hero section with stats
2. **Filters Work** ✅ - Month/Year dropdowns should populate
3. **Database Connection** ✅ - No connection errors in console
4. **Top 10 Clients** ✅ - Click button to view client rankings

## 🚀 Deploy to Azure

### Option A: Automated Script
```bash
# Make script executable (Linux/Mac)
chmod +x deploy_azure.sh

# Run deployment
./deploy_azure.sh
```

### Option B: Manual Steps
1. Create Azure Web App
2. Set environment variables
3. Deploy code
4. Test live URL

## 🔧 Troubleshooting

### Common Issues:

**❌ "Database connection failed"**
- Check .env file credentials
- Verify Azure SQL Database is accessible
- Check firewall rules

**❌ "Module not found"**
- Activate virtual environment
- Run `pip install -r requirements.txt`

**❌ "Port already in use"**
- Change port in app.py: `app.run(port=5001)`
- Or kill existing process: `lsof -ti:5000 | xargs kill`

## 📱 What You'll See

- **Professional Header** with navigation
- **Hero Section** with key metrics
- **Cost Analysis** with filters and results
- **Insights Section** with Top 10 Clients
- **Smooth Scrolling** between sections
- **Responsive Design** for all devices

## 🎯 Next Steps

1. **Customize Data** - Update SQL queries in app.py
2. **Add Features** - Implement Phase 2 requirements
3. **Style Changes** - Modify static/css/style.css
4. **Deploy Updates** - Use Azure deployment script

## 📞 Need Help?

1. Check browser console for errors
2. Review terminal output
3. Run `python test_setup.py` for diagnostics
4. Check README.md for detailed instructions

---

**🎉 You're all set!** Your leadership dashboard is ready to impress stakeholders with professional cost analysis capabilities.