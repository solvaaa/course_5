from abc import ABC, abstractmethod
import requests
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
        id, name, url, salary, description, date_published
        salary - словарь с ключами to и from
        '''
        pass

    def get_employer_info(self, employer_id):
        pass


class HeadHunter():
    '''
    Класс для получения информации из API HeadHunter.ru
    '''
    def __init__(self, per_page=100):
        '''
        :param per_page: задаёт количество запрашиваемых вакансий. До 100
        '''
        self.per_page = per_page

    def get_number_of_pages(self, employer_id):
        params = {"employer_id": str(employer_id), "per_page": self.per_page}
        response = requests.get('https://api.hh.ru/vacancies', params)
        assert response.status_code == 200, 'Request not successful'
        return response.json()['pages']

    def get_info(self, page, employer_id: int):
        '''
        Метод для получения сырой информации из API по id работодателя.
        Возвращает список словарей
        '''
        params = {"area": 113, "employer_id": str(employer_id), "per_page": self.per_page, "page": page}
        response = requests.get('https://api.hh.ru/vacancies', params)
        assert response.status_code == 200, f'Request not successful ({response.status_code})'
        return response.json()['items']

    def output_info(self, employer_id: int):
        '''
        Метод возвращает отформатированную информацию о вакансиях
        по ключевому слову.
        Содержит следующие поля:
        id, name, url, salary, description, date_published
        salary - словарь с ключами to и from
        '''
        page = 0
        max_page = self.get_number_of_pages(employer_id)
        output = []
        found_check = set()
        while page < max_page and page * self.per_page < 2000:
            hh_output = self.get_info(page, employer_id)
            if page == 0:
                print(*hh_output[0], sep='\n')
            for info in hh_output:
                assert info['archived'] == False
                vacancy_id = int(info['id'])
                name = info['name']
                url = info['alternate_url']
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
                    'vacancy_id': vacancy_id,
                    'employer_id': employer_id,
                    'name': name,
                    'url': url,
                    'salary_from': salary['from'],
                    'salary_to': salary['to'],
                    'description': description,
                }
                set_check = (item['name'], item['salary_from'], item['salary_to'])
                if set_check not in found_check:
                    output.append(item)
                    found_check.add(set_check)
            page += 1
        return output

    def get_employer_info(self, employer_id: int):
        response = requests.get('https://api.hh.ru/employers/' + str(employer_id))
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
vacancies = hh.output_info(1122462)
v = []
print(hh.get_number_of_pages(1122462))
for vacancy in vacancies:
    v.append((vacancy['vacancy_id'], vacancy['name'], vacancy['salary_from']))
v.sort()
print(*v, sep='\n')
print('len', len(vacancies))
