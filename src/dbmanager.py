from config import config
from parser import QueryParser
import psycopg2
CREATE_TABLES_PATH = 'create_tables.sql'

class DBManager:

    def __init__(self):
        pass

    def create_database(self, params):
        dbname = params['database']
        del params['database']
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"DROP DATABASE {dbname}")
        except psycopg2.errors.InvalidCatalogName:
            pass
        cur.execute(f"CREATE DATABASE {dbname}")
        conn.close()

        conn = psycopg2.connect(dbname=dbname, **params)

        with open(CREATE_TABLES_PATH, 'r', encoding='utf-8') as queries_file:
            query = queries_file.read()

        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        conn.close()
