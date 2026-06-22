import mysql.connector as mc

def get_db_connection():
    return mc.connect (
        host="localhost",
        user="root",
        password="Sagar@9863",
        database="resume_management_system"
    )