from src.config import config
from src.parser import QueryParser
import psycopg2
CREATE_TABLES_PATH = 'src/create_tables.sql'
QUERIES_PATH = 'src/queries.sql'


class DBManager:

    def __init__(self, create_tables_path=CREATE_TABLES_PATH,
                 queries_path=QUERIES_PATH):
        self.__create_tables_path = create_tables_path
        self.__parser = QueryParser()
        self.__parser.read(queries_path)

    def create_database(self, params=config()):
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

        with open(self.__create_tables_path, 'r', encoding='utf-8') as queries_file:
            query = queries_file.read()

        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        conn.close()

    def execute_query(self, query_name, query_params={}, params=config()):
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

    def get_companies_and_vacancies_count(self, params=config()):
        colnames, response = self.execute_query('get_companies_and_vacancies_count')
        print(response)
        return self.tuple_to_dict(colnames, response)

    def get_all_vacancies(self, params=config()):
        colnames, response = self.execute_query('get_all_vacancies')
        colnames[0] = 'employer'
        return self.tuple_to_dict(colnames, response)

    def get_avg_salary(self, params=config()):
        colnames, response = self.execute_query('get_avg_salary')
        return response[0]

    def get_vacancies_with_higher_salary(self, params=config()):
        colnames, response = self.execute_query('get_vacancies_with_higher_salary')
        return self.tuple_to_dict(colnames, response)

    def get_vacancies_with_keyword(self, keyword, params=config()):
        keyword = '%' + keyword.lower() + '%'
        colnames, response = self.execute_query('get_vacancies_with_keyword', {"keyword": keyword})
        return self.tuple_to_dict(colnames, response)

    @staticmethod
    def tuple_to_dict(colnames, response):
        output = []
        for item in response:
            item_dict = {}
            for i in range(len(colnames)):
                item_dict[colnames[i]] = item[i]
            print(item_dict)
            output.append(item_dict)
        return output
