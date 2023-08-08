from src.dbmanager import DBManager
import src.database_fill as database_fill


def interaction():
    dbmanager = DBManager()
    database_fill.create_database()
    database_fill.fill_employer_table()
    database_fill.fill_vacancies_table()

    result = dbmanager.get_all_vacancies()
    #result = dbmanager.get_companies_and_vacancies_count()
    #result = dbmanager.get_avg_salary()
    #result = dbmanager.get_vacancies_with_higher_salary()
    #result = dbmanager.get_vacancies_with_keyword('junior')

    print(*result, sep='\n')


if __name__ == "__main__":
    interaction()