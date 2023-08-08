from src.dbmanager import DBManager
from src.api import HeadHunter
import psycopg2
from src.config import config
EMPLOYERS = [1740, 3529, 80, 3776, 3127, 1122462, 9352463, 2748, 6836, 230005]


def fill_employer_table():
    employers = EMPLOYERS
    hh_api = HeadHunter()
    params = config()
    conn = psycopg2.connect(**params)
    with conn.cursor() as cur:
        for employer in employers:
            employer_info = hh_api.get_employer_info(employer)
            cur.execute('''
                INSERT INTO employers (employer_id, name, url, description)
                VALUES (%(employer_id)s, %(name)s, %(url)s, %(description)s)
                ''',
                employer_info)
    conn.commit()
    conn.close()


def interaction():
    dbmanager = DBManager()
    dbmanager.create_database()
    fill_employer_table()


if __name__ == "__main__":
    interaction()