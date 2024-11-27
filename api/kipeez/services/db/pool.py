import os
from psycopg2.pool import SimpleConnectionPool
# import psycopg2.extras
from dotenv import load_dotenv

DATABASE_URI = None
if not DATABASE_URI:
    load_dotenv()
    DATABASE_URI = os.environ["DATABASE_URI"]
    pool = None
try:
    pool = SimpleConnectionPool(
        minconn=1,
        maxconn=10, 
        dsn=DATABASE_URI)
    print("DB pool started on ", pool.getconn().dsn)
except Exception as e:
    print(e)

