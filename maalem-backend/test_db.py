import os
import django
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Test database connection
from django.db import connection

try:
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print("Database connection successful:", result)
except Exception as e:
    print("Database connection failed:", str(e))
finally:
    if 'cursor' in locals():
        cursor.close()