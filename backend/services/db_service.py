import mysql.connector


def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="attendance_db",
        )
        return conn
    except Exception as e:
        print("DB Connection Error:", e)
        raise Exception("DB connection failed")
