from abc import ABC, abstractmethod
import requests
import psycopg2
import csv
from pprint import pprint


class Api(ABC):
    '''
    Базовый класс для работы с API сайтов по поиску работы
    '''
    @abstractmethod
    def get_info(self, employer_id):
        '''
        Метод для получения сырой информации из API по id работодателя.
        Возвращает список словарей
        '''
        pass

    @abstractmethod
    def output_info(self, employer_id):
        '''
        Метод возвращает отформатированную информацию о вакансиях
        по ключевому слову.
        Содержит следующие поля:
        id, name, link, salary, description, date_published
        salary - словарь с ключами to и from
        '''
        pass

    def get_employer_info(self, employer_id):
        pass


class HeadHunter():
    '''
    Класс для получения информации из API HeadHunter.ru
    '''
    def __init__(self, per_page=10):
        '''
        :param per_page: задаёт количество запрашиваемых вакансий. До 100
        '''
        self.per_page = per_page

    def get_info(self, employer_id):
        '''
        Метод для получения сырой информации из API по id работодателя.
        Возвращает список словарей
        '''
        params = {"employer_id": employer_id, "per_page": self.per_page}
        response = requests.get('https://api.hh.ru/vacancies', params)
        assert response.status_code == 200, 'Request not successful'
        return response.json()['items']

    def output_info(self, employer_id):
        '''
        Метод возвращает отформатированную информацию о вакансиях
        по ключевому слову.
        Содержит следующие поля:
        id, name, link, salary, description, date_published
        salary - словарь с ключами to и from
        '''
        hh_output = self.get_info(employer_id)
        output = []
        for info in hh_output:
            id = int(info['id'])
            name = info['name']
            link = info['alternate_url']
            if info['salary'] is not None:
                salary = {
                    'from': info['salary']['from'],
                    'to': info['salary']['to']
                }
            else:
                salary = {'from': None, 'to': None}
            if info['snippet'] is not None:
                snippet = []
                for key, value in info['snippet'].items():
                    if value is not None:
                        snippet.append(value)
                description = ' '.join(snippet)
            else:
                description = None

            item = {
                'id': id,
                'employer_id': employer_id,
                'name': name,
                'link': link,
                'salary': salary,
                'description': description,
            }
            output.append(item)
        return output

    def get_employer_info(self, employer_id):
#        params = {"employer_id": employer_id, "per_page": self.per_page}
        response = requests.get('https://api.hh.ru/employers/' + employer_id)
        employer_data = response.json()
        assert response.status_code == 200, 'Request not successful'

        employer = {
            "employer_id": employer_id,
            "name": employer_data["name"],
            "url": employer_data["alternate_url"],
            "description": employer_data["description"][:200]
        }
        return employer


hh = HeadHunter()
info = hh.get_employer_info('1740')
pprint(info, width=140)