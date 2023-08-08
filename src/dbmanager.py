from api import HeadHunter
from config import config
import psycopg2


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
            print('dropped')
        except psycopg2.errors.InvalidCatalogName:
            pass
        cur.execute(f"CREATE DATABASE {dbname}")
        conn.close()

        conn = psycopg2.connect(dbname=dbname, **params)


man = DBManager()
params = config()
print(config())
man.create_database(params)