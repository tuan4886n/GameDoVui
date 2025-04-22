import psycopg2
import os
from dotenv import load_dotenv

# Connection URL from Railway
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Kết nối PostgreSQL thành công!")
        return conn, cursor
    except Exception as e:
        print(f"❌ Kết nối thất bại: {e}")
        return None, None