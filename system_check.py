import os
import sys
import boto3
import requests
import pymysql
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

def check_environment_variables():
    print("\n🔍 Checking Environment Variables...")
    required_vars = {
        'Database': ['DATABASE_URL', 'DB_HOST', 'DB_USER', 'DB_PASS', 'DB_NAME'],
        'AWS S3': ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'S3_BUCKET'],
        'Weather API': ['WEATHER_API_KEY'],
        'Firebase': ['FIREBASE_PROJECT_ID', 'FIREBASE_API_KEY'],
        'Flask': ['SECRET_KEY']
    }
    
    missing_vars = []
    for category, vars in required_vars.items():
        category_vars = []
        for var in vars:
            if not os.getenv(var):
                category_vars.append(var)
        if category_vars:
            missing_vars.append(f"{category}: {', '.join(category_vars)}")
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for missing in missing_vars:
            print(f"   - {missing}")
    else:
        print("✅ All required environment variables are set")
    return len(missing_vars) == 0

def check_database_connection():
    print("\n🔍 Checking Database Connection...")
    try:
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            db_user = os.getenv('DB_USER')
            db_pass = os.getenv('DB_PASS') or os.getenv('DB_PASSWORD')
            db_host = os.getenv('DB_HOST')
            db_name = os.getenv('DB_NAME')
            db_port = int(os.getenv('DB_PORT', '3306'))
            conn = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_pass,
                database=db_name,
                port=db_port
            )
        else:
            # Parse DATABASE_URL for PyMySQL connection
            from urllib.parse import urlparse
            url = urlparse(db_url)
            conn = pymysql.connect(
                host=url.hostname,
                user=url.username,
                password=url.password,
                database=url.path[1:],  # Remove leading slash
                port=url.port or 3306
            )
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                print("✅ Database connection successful")
                return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
    return False

def check_s3_connection():
    print("\n🔍 Checking AWS S3 Connection...")
    try:
        if not os.getenv('AWS_ACCESS_KEY_ID'):
            print("❌ AWS credentials not configured")
            return False
            
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        # Test bucket access
        bucket = os.getenv('S3_BUCKET')
        s3_client.head_bucket(Bucket=bucket)
        print(f"✅ S3 connection and bucket '{bucket}' access successful")
        return True
    except Exception as e:
        print(f"❌ S3 connection failed: {str(e)}")
    return False

def check_weather_api():
    print("\n🔍 Checking Weather API...")
    try:
        api_key = os.getenv('WEATHER_API_KEY')
        if not api_key:
            print("❌ Weather API key not configured")
            return False
            
        # Test API with Pune coordinates
        url = f"https://api.openweathermap.org/data/2.5/weather?lat=18.5204&lon=73.8567&appid={api_key}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✅ Weather API connection successful")
            return True
        else:
            print(f"❌ Weather API returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Weather API check failed: {str(e)}")
    return False

def check_firebase():
    print("\n🔍 Checking Firebase Configuration...")
    try:
        if not os.getenv('FIREBASE_PROJECT_ID'):
            print("❌ Firebase configuration not found")
            return False
            
        # Only initialize if not already initialized
        if not firebase_admin._apps:
            # Check if service account file exists
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT', './serviceAccountKey.json')
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized successfully")
                return True
            else:
                print("❌ Firebase service account file not found")
    except Exception as e:
        print(f"❌ Firebase initialization failed: {str(e)}")
    return False

def main():
    print("=" * 50)
    print("🔎 Starting System Health Check")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Run checks
    checks = [
        ("Environment Variables", check_environment_variables()),
        ("Database Connection", check_database_connection()),
        ("S3 Storage", check_s3_connection()),
        ("Weather API", check_weather_api()),
        ("Firebase", check_firebase())
    ]
    
    print("\n" + "=" * 50)
    print("📊 System Health Summary")
    print("=" * 50)
    
    all_passed = True
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
        all_passed = all_passed and result
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All systems operational")
    else:
        print("⚠️ Some systems require attention")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())