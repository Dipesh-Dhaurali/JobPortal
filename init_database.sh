#!/bin/bash

echo "=========================================="
echo "JobPortal Database Setup"
echo "=========================================="

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Making migrations for authuser app...${NC}"
python manage.py makemigrations authuser

echo -e "${BLUE}Step 2: Making migrations for admin_portal app...${NC}"
python manage.py makemigrations admin_portal

echo -e "${BLUE}Step 3: Applying all migrations...${NC}"
python manage.py migrate

echo -e "${BLUE}Step 4: Initializing database with test data...${NC}"
python manage_db.py

echo -e "${GREEN}=========================================="
echo "✓ Database setup completed successfully!"
echo "==========================================${NC}"
