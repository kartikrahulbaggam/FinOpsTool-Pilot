#!/bin/bash

# Azure Web App Deployment Script for Cost Analysis Dashboard
# This script automates the deployment process to Azure

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration variables
RESOURCE_GROUP="cost-analysis-rg"
LOCATION="eastus"
APP_SERVICE_PLAN="cost-analysis-plan"
WEB_APP_NAME="cost-analysis-app"
PYTHON_VERSION="3.9"
SKU="B1"

echo -e "${BLUE}🚀 Azure Web App Deployment Script${NC}"
echo "=================================="

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if user is logged in to Azure
echo -e "${YELLOW}🔍 Checking Azure login status...${NC}"
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Azure. Please login...${NC}"
    az login
fi

# Get current subscription
SUBSCRIPTION=$(az account show --query id -o tsv)
echo -e "${GREEN}✅ Using subscription: ${SUBSCRIPTION}${NC}"

# Create resource group
echo -e "${YELLOW}🔧 Creating resource group: ${RESOURCE_GROUP}${NC}"
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output table

# Create App Service plan
echo -e "${YELLOW}🔧 Creating App Service plan: ${APP_SERVICE_PLAN}${NC}"
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku $SKU \
    --is-linux \
    --output table

# Create Web App
echo -e "${YELLOW}🔧 Creating Web App: ${WEB_APP_NAME}${NC}"
az webapp create \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --runtime "PYTHON|$PYTHON_VERSION" \
    --deployment-local-git \
    --output table

# Get the Git remote URL
GIT_REMOTE=$(az webapp deployment list-publishing-credentials \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --query publishingUserName -o tsv)

echo -e "${GREEN}✅ Web App created successfully!${NC}"
echo -e "${BLUE}📱 Web App URL: https://${WEB_APP_NAME}.azurewebsites.net${NC}"

# Configure environment variables
echo -e "${YELLOW}🔧 Configuring environment variables...${NC}"

# Check if .env file exists
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env file found. Configuring environment variables...${NC}"
    
    # Read .env file and set each variable
    while IFS= read -r line; do
        # Skip empty lines and comments
        if [[ $line =~ ^[^#]*=.*$ ]] && [[ ! -z $line ]]; then
            KEY=$(echo $line | cut -d'=' -f1)
            VALUE=$(echo $line | cut -d'=' -f2-)
            
            echo -e "${YELLOW}Setting ${KEY}...${NC}"
            az webapp config appsettings set \
                --resource-group $RESOURCE_GROUP \
                --name $WEB_APP_NAME \
                --settings "$KEY=$VALUE" \
                --output none
        fi
    done < .env
    
    echo -e "${GREEN}✅ Environment variables configured${NC}"
else
    echo -e "${YELLOW}⚠️  .env file not found. Please configure environment variables manually:${NC}"
    echo "1. Go to Azure Portal"
    echo "2. Navigate to your Web App"
    echo "3. Go to Configuration → Application settings"
    echo "4. Add the following variables:"
    echo "   - DB_SERVER"
    echo "   - DB_NAME"
    echo "   - DB_USERNAME"
    echo "   - DB_PASSWORD"
    echo "   - DB_DRIVER"
fi

# Configure startup command
echo -e "${YELLOW}🔧 Configuring startup command...${NC}"
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app" \
    --output none

# Enable logging
echo -e "${YELLOW}🔧 Enabling application logging...${NC}"
az webapp log config \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --web-server-logging filesystem \
    --output none

# Deploy the application
echo -e "${YELLOW}🚀 Deploying application...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}"

# Use az webapp up for deployment
az webapp up \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --runtime "PYTHON|$PYTHON_VERSION" \
    --sku $SKU \
    --output table

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Wait a few minutes for the app to fully start"
echo "2. Test your application: https://${WEB_APP_NAME}.azurewebsites.net"
echo "3. Check logs if there are any issues:"
echo "   az webapp log tail --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
echo ""
echo -e "${BLUE}🔧 Useful commands:${NC}"
echo "View logs: az webapp log tail --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
echo "Restart app: az webapp restart --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
echo "Delete resources: az group delete --name $RESOURCE_GROUP --yes"
echo ""
echo -e "${GREEN}✅ Your Cost Analysis Dashboard is now live on Azure!${NC}"