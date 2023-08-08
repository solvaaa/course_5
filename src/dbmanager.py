from src.config import config
from src.parser import QueryParser
import psycopg2
QUERIES_PATH = 'src/queries.sql'


class DBManager:
    '''
    Класс для взаимодействия с базой данных
    '''
    def __init__(self):
        '''
        Создаёт экзеспляр класса QueryParser,
        читает файл из пути по умолчанию
        '''
        self.__parser = QueryParser()
        self.__parser.read(QUERIES_PATH)

    def execute_query(self, query_name: str, query_params={}, params=config()) -> tuple:
        '''
        Запускает в базе данных sql запрос, полученный из QueryParser
        query_name - название запроса, согласно файлу queries.sql
        query_params - словарь параметров параметризованного запроса
        params - словарь параметров базы данных (по умолчанию из database.ini)
        Возращает кортеж из:
        - список названий колонок
        - список кортежей строк
        '''
        conn = psycopg2.connect(**params)
        conn.set_session(readonly=True, autocommit=True)
        query = self.__parser.get_item(query_name)
        with conn.cursor() as cur:
            cur.execute(query, query_params)
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
        conn.commit()
        conn.close()
        return colnames, rows

    def get_companies_and_vacancies_count(self, params=config()) -> list:
        '''
        получает список всех компаний и количество вакансий у каждой компании
        '''
        colnames, response = self.execute_query('get_companies_and_vacancies_count')
        print(response)
        return self.tuple_to_dict(colnames, response)

    def get_all_vacancies(self, params=config()) -> list:
        '''
        получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        Возвращает список словарей {colname: value}
        '''
        colnames, response = self.execute_query('get_all_vacancies')
        colnames[0] = 'employer'
        return self.tuple_to_dict(colnames, response)

    def get_avg_salary(self, params=config()) -> int:
        '''
        получает среднюю зарплату по вакансиям.
        '''
        colnames, response = self.execute_query('get_avg_salary')
        return response[0]

    def get_vacancies_with_higher_salary(self, params=config()) -> list:
        '''
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        Возвращает список словарей {colname: value}
        '''
        colnames, response = self.execute_query('get_vacancies_with_higher_salary')
        return self.tuple_to_dict(colnames, response)

    def get_vacancies_with_keyword(self, keyword: str, params=config()) -> list:
        '''
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        Возвращает список словарей {colname: value}
        '''
        keyword = '%' + keyword.lower() + '%'
        colnames, response = self.execute_query('get_vacancies_with_keyword', {"keyword": keyword})
        return self.tuple_to_dict(colnames, response)

    @staticmethod
    def tuple_to_dict(colnames: list, response: list) -> list:
        '''
        Переводит результат execute_query из формата
        список кортежей в формат список словарей
        '''
        output = []
        for item in response:
            item_dict = {}
            for i in range(len(colnames)):
                item_dict[colnames[i]] = item[i]
            print(item_dict)
            output.append(item_dict)
        return output
