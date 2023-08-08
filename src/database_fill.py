import psycopg2
from src.api import HeadHunter
from src.config import config


EMPLOYERS = [1740, 3529, 80, 3776, 3127, 1122462, 9352463, 2748, 6836, 230005]


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