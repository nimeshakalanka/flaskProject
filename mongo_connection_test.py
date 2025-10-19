from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import sys

# Test different connection strings
#test_cases = [
    # Original connection string
    #"mongodb+srv://susltg:susltg@cluster0.pwsuf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    
    # With specific database
    #"mongodb+srv://susltg:susltg@cluster0.pwsuf.mongodb.net/image_gallery?retryWrites=true&w=majority&appName=Cluster0",
    
    # With admin database for auth
    #"mongodb+srv://susltg:susltg@cluster0.pwsuf.mongodb.net/admin?retryWrites=true&w=majority&appName=Cluster0",
]

print("Testing MongoDB connections...\n")

for i, uri in enumerate(test_cases, 1):
    print(f"Test {i}:")
    print(f"URI: {uri[:50]}...")
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        print("✓ Connection successful!")
        
        # Try to list databases
        dbs = client.list_database_names()
        print(f"✓ Available databases: {dbs}")
        
        # Try to access the image_gallery database
        db = client['image_gallery']
        collections = db.list_collection_names()
        print(f"✓ Collections in image_gallery: {collections}")
        
        client.close()
        print("=" * 50)
        break  # If successful, no need to test others
        
    except OperationFailure as e:
        print(f"✗ Authentication failed: {e}")
        print(f"  Error code: {e.code}")
        print(f"  Error details: {e.details}")
    except ConnectionFailure as e:
        print(f"✗ Connection failed: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
    
    print("=" * 50)
    print()

print("\nDiagnostic recommendations:")
print("1. Go to MongoDB Atlas → Database Access")
print("2. Check if user 'susltg' exists and is active")
print("3. Verify the password is correct")
print("4. Check 'Database User Privileges' - should have readWrite on image_gallery or atlasAdmin")
print("5. Go to Network Access and verify your IP is whitelisted (or use 0.0.0.0/0 for testing)")