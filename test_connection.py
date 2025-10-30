#!/usr/bin/env python3
"""
MongoDB Connection Test Script
Tests if MongoDB connection is working properly
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """
    Tests MongoDB connection and reports detailed status
    """
    print("=" * 60)
    print("CodeGalaxy - MongoDB Connection Test")
    print("=" * 60)
    print()

    # Check if MONGO_URI exists
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        print("❌ ERROR: MONGO_URI not found in .env file")
        print("   Please add your MongoDB connection string to .env")
        return False

    print("✅ MONGO_URI found in environment")
    print(f"   Connection string: {mongo_uri[:30]}... (truncated)")
    print()

    # Try to connect
    print("🔄 Attempting to connect to MongoDB...")
    try:
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,  # 10 second timeout
            connectTimeoutMS=10000
        )

        # Test the connection
        print("🔄 Testing connection with ping command...")
        client.admin.command('ping')

        print("✅ Successfully connected to MongoDB!")
        print()

        # Get database info
        db = client['codegalaxy']
        print("📊 Database Information:")
        print(f"   Database: codegalaxy")

        # List collections
        collections = db.list_collection_names()
        print(f"   Collections: {len(collections)}")
        if collections:
            for coll in collections:
                count = db[coll].count_documents({})
                print(f"      - {coll}: {count} documents")
        else:
            print("      (No collections yet - will be created on first use)")

        print()
        print("✅ MongoDB connection is working perfectly!")
        print("   You can now run the application with: streamlit run main.py")

        client.close()
        return True

    except ServerSelectionTimeoutError as e:
        print("❌ CONNECTION TIMEOUT")
        print()
        print("Possible causes:")
        print("  1. No internet connection")
        print("  2. MongoDB Atlas cluster is paused")
        print("  3. IP address not whitelisted in MongoDB Atlas")
        print()
        print("Solutions:")
        print("  1. Check your internet connection")
        print("  2. Go to MongoDB Atlas and ensure cluster is running")
        print("  3. Add 0.0.0.0/0 to IP whitelist:")
        print("     - Go to https://cloud.mongodb.com")
        print("     - Select your cluster")
        print("     - Click 'Network Access' in left menu")
        print("     - Click 'Add IP Address'")
        print("     - Click 'Allow Access From Anywhere'")
        print()
        print(f"Technical error: {str(e)[:200]}")
        return False

    except ConnectionFailure as e:
        print("❌ CONNECTION FAILED")
        print()
        print("MongoDB connection failed. Please verify:")
        print("  1. Your MONGO_URI in .env file is correct")
        print("  2. Your MongoDB Atlas cluster is active")
        print("  3. Your credentials are correct")
        print()
        print(f"Technical error: {str(e)[:200]}")
        return False

    except OperationFailure as e:
        print("❌ AUTHENTICATION FAILED")
        print()
        print("MongoDB credentials are incorrect. Please verify:")
        print("  1. Username and password in MONGO_URI are correct")
        print("  2. Database user has proper permissions")
        print()
        print(f"Technical error: {str(e)[:200]}")
        return False

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {type(e).__name__}")
        print()
        print(f"Error details: {str(e)[:200]}")
        return False

def test_huggingface_api():
    """
    Tests Hugging Face API key
    """
    print()
    print("=" * 60)
    print("Hugging Face API Test")
    print("=" * 60)
    print()

    hf_key = os.getenv('HUGGINGFACE_API_KEY')
    if not hf_key:
        print("❌ HUGGINGFACE_API_KEY not found in .env file")
        return False

    print("✅ HUGGINGFACE_API_KEY found in environment")
    print(f"   API Key: {hf_key[:10]}... (truncated)")
    print()
    print("ℹ️  Hugging Face API will be tested when you generate code")
    return True

if __name__ == "__main__":
    print()
    mongo_ok = test_mongodb_connection()
    hf_ok = test_huggingface_api()

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()

    if mongo_ok and hf_ok:
        print("✅ All connections are working!")
        print("   You're ready to run: streamlit run main.py")
    elif mongo_ok:
        print("⚠️  MongoDB is working, but Hugging Face API not tested")
        print("   You can still run the app: streamlit run main.py")
    else:
        print("❌ Please fix the MongoDB connection before running the app")
        print("   Follow the solutions mentioned above")

    print()
