import psycopg2
from src.api import HeadHunter
from src.config import config
CREATE_TABLES_PATH = 'src/create_tables.sql'
QUERIES_PATH = 'src/queries.sql'
EMPLOYERS = [1740, 3529, 80, 3776, 3127, 1122462, 9352463, 2748, 6836, 230005]


def create_database(create_tables_path=CREATE_TABLES_PATH, params=config()):
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

    with open(create_tables_path, 'r', encoding='utf-8') as queries_file:
        query = queries_file.read()

    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()
    conn.close()


def fill_employer_table(employers=EMPLOYERS):
    hh_api = HeadHunter()
    params = config()
    conn = psycopg2.connect(**params)
    with conn.cursor() as cur:
        for employer_id in employers:
            employer_info = hh_api.get_employer_info(employer_id)
            cur.execute("""
                INSERT INTO employers VALUES (
                %(employer_id)s, %(name)s, %(url)s, %(description)s
                )""",
                employer_info)
    conn.commit()
    conn.close()


def fill_vacancies_table(employers=EMPLOYERS):
    hh_api = HeadHunter()
    params = config()
    conn = psycopg2.connect(**params)
    with conn.cursor() as cur:
        for employer_id in employers:
            vacancies = hh_api.output_info(employer_id)
            for vacancy in vacancies:
                if len(vacancy['name']) > 50:
                    vacancy['name'] = vacancy['name'][:50]
                cur.execute("""
                    INSERT INTO vacancies VALUES (
                    %(vacancy_id)s,
                    %(employer_id)s,
                    %(name)s,
                    %(url)s,
                    %(salary_from)s,
                    %(salary_to)s,
                    %(description)s
                    )""",
                    vacancy)
    conn.commit()
    conn.close()