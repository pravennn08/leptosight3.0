import psycopg2
import os
import sys
from dotenv import load_dotenv
from termcolor import colored

load_dotenv()


def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        return conn
    except Exception as error:
        print(colored(f"Connection Error: {error}", "red"))
        sys.exit(1)
