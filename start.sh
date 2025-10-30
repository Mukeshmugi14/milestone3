#!/bin/bash

echo "🚀 Starting CodeGalaxy..."
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Initialize database indexes
echo "🗄️  Initializing database..."
python3 -c "import database; database.create_indexes(); print('✅ Database indexes created!')"

# Start Streamlit
echo ""
echo "✨ Starting CodeGalaxy application..."
echo "================================"
echo ""
echo "🌐 Access the app at: http://localhost:8501"
echo "👑 Admin portal: http://localhost:8501?admin=true"
echo "🔑 Admin password: Infosys"
echo ""
streamlit run main.py
