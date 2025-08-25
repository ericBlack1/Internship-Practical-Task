#!/bin/bash

# Employee Management System Setup Script
# This script helps set up the Django project with PostgreSQL

echo "🚀 Setting up Employee Management System..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 &> /dev/null; then
    echo "⚠️  PostgreSQL is not running or not accessible."
    echo "   Please start PostgreSQL and ensure it's running on localhost:5432"
    echo "   You can start it with: sudo systemctl start postgresql"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
DEBUG=True
SECRET_KEY=django-insecure-b@@x7fl^1x%kh-q7*&%08mgv+al$^=q_e82ok6b)9#2zt5pez5

# Database Configuration
DB_NAME=employee_management
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Django Settings
ALLOWED_HOSTS=localhost,127.0.0.1
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
EOF
    echo "✅ .env file created. Please update the database password if needed."
else
    echo "✅ .env file already exists."
fi

# Create database if it doesn't exist
echo "🗄️  Setting up database..."
if createdb -U postgres -h localhost employee_management 2>/dev/null; then
    echo "✅ Database 'employee_management' created successfully."
else
    echo "ℹ️  Database 'employee_management' already exists or creation failed."
    echo "   You may need to create it manually or check PostgreSQL permissions."
fi

# Run migrations
echo "🔄 Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
echo "Please provide the following information for the admin user:"
python manage.py createsuperuser

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Update the .env file with your actual PostgreSQL password"
echo "2. Run the development server: python manage.py runserver"
echo "3. Access the admin interface at: http://127.0.0.1:8000/admin/"
echo "4. (Optional) Run sample data script: python sample_data.py"
echo ""
echo "Happy coding! 🚀"
