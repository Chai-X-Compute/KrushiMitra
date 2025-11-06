import json
import os
from dotenv import load_dotenv

def create_service_account():
    """
    Creates a serviceAccountKey.json file from environment variables.
    """
    load_dotenv()
    
    service_account = {
        "type": "service_account",
        "project_id": os.getenv('FIREBASE_PROJECT_ID'),
        "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID', ''),
        "private_key": os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
        "client_email": os.getenv('FIREBASE_CLIENT_EMAIL', ''),
        "client_id": os.getenv('FIREBASE_CLIENT_ID', ''),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv('FIREBASE_CERT_URL', ''),
        "universe_domain": "googleapis.com"
    }
    
    # Check if we have the minimum required fields
    required_fields = ['project_id', 'private_key_id', 'private_key', 'client_email']
    missing_fields = [field for field in required_fields 
                     if not service_account.get(field) or service_account[field].strip() == '']
    
    if missing_fields:
        print("\n❌ Error: Missing required Firebase credentials")
        print("Please add the following environment variables to your .env file:")
        for field in missing_fields:
            env_var = f'FIREBASE_{field.upper()}'
            print(f"- {env_var}")
        print("\nTo get these credentials:")
        print("1. Go to Firebase Console (https://console.firebase.google.com)")
        print("2. Select your project")
        print("3. Go to Project Settings > Service Accounts")
        print("4. Click 'Generate New Private Key'")
        print("5. Use the contents of the downloaded file to set the environment variables")
        return False
    
    try:
        with open('serviceAccountKey.json', 'w') as f:
            json.dump(service_account, f, indent=2)
        print("\n✅ Successfully created serviceAccountKey.json")
        print("🔒 This file contains sensitive information - make sure it's in .gitignore")
        return True
    except Exception as e:
        print(f"\n❌ Error creating service account file: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Setting up Firebase service account...")
    create_service_account()