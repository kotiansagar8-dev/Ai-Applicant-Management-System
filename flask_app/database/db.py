import os
from dotenv import load_dotenv
import mysql.connector as mc

# Load environment variables

load_dotenv()

def get_db_connection():
    return mc.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
