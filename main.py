from src.dbmanager import DBManager
from src.database_fill import fill_employer_table, fill_vacancies_table


def interaction():
    dbmanager = DBManager()
#    dbmanager.create_database()
#    fill_employer_table()
#    fill_vacancies_table()
    result = dbmanager.get_all_vacancies()
    print(*result, sep='\n')


if __name__ == "__main__":
    interaction()