# course_4
<h1>Курсовая работа №5 (создание базы данных вакансий)</h1>


<h2>Для курса Python разработчик от SkyPro</h2>


Автор: Александра Соловьёва

Для работы с программой, необходим доступ к серверу postgresSQL

<h3>1. Классы для работы с API:</h3>

<h4>Базовый абстрактный класс: Api</h4>

Методы класса:<br/>

<b> - get_info(self, keyword) </b><br/>
        Метод для получения сырой информации о вакансиях из API по id работодателя.
        Возвращает список словарей<br/><br/>

<b> - output_info(self, keyword) </b><br/>
Метод возвращает отформатированную информацию о вакансиях по ключевому слову.<br/>
<ins>Содержит следующие поля:</ins><br/>
        &nbsp &nbsp <i>id</i>: id вакансии. Целочисленный <br/>
        &nbsp &nbsp <i>name</i>: Название вакансии <br/>
        &nbsp &nbsp <i>url</i>: Ссылка на вакансию <br/>
        &nbsp &nbsp <i>salary_from</i>: Минимальная зарплата<br/>
        &nbsp &nbsp <i>salary_from</i>: Минимальная зарплата<br/>
        &nbsp &nbsp <i>description</i>: Описание вакансии в виде списка словарей

<h4>Класс HeadHunter</h4>
Работает с API сайта headhunter.ru


<h3>2. Создание базы данных. Модуль database_fill</h3>

<h4>Функция create_database</h4>
Функция создаёт базу данных по параметрам params. <br/>
По умолчанию выставляются параметры, находящиеся в файле <i>src/database.ini</i><br/>
Парсит при помощи модуля config и класса ConfigParser<br/>
Затем, запускает файл по пути create_tables_path <br/>
(по умолчанию путь из константы CREATE_TABLES_PATH = <i>'src/create_tables.sql'</i>) <br/>
В файле находятся запросы на создание таблиц: <br/>
    <b>employers (employer_id, name, url, description)</b><br/>
    <b>vacancies (vacancy_id, name, url, salary_from, salary_to, description)</b>

<h4>Функция fill_employer_table</h4>
Функция наполняет таблицу employer данными с hh.ru <br/>
Добавляет работодателей с id из списка employers

<h4>Функция fill_vacancies_table</h4>
Функция наполняет таблицу vacancies данными с hh.ru <br/>
Добавляет вакансии работодателей с id из списка employers


<h3>3. Парсинг .ini и .sql файлов. Модули parser, config</h3>

<h4>Класс ConfigParser</h4>
Класс для парсинга файлов .ini <br/>

Методы класса:<br/>

<b> - read(self, path) </b><br/>
        Читает содержимое файла, по адресу path <br/>
        Результат, разделённый по секциям,
        записывается в атрибут экземпляра класса self.config (dict)<br/>
        В формате <i>{section: [(key, value), (key, value)]}</i> <br/><br/>

<b> - has_section(self, section) </b><br/>
Проверяет наличие секции <i>section</i> внутри прочитанного файла <br/><br/>

<b> - get_item(self, section) </b><br/>
        Возвращает параметры внутри секции <i>section</i> файла
        в виде списка кортежей <i>(key, value)</i><br/><br/>



<h4>Класс QueryParser</h4>
Класс для парсинга файлов .sql <br/>
Используется классом <b>DBManager</b> для выполнения запросов<br/>

Методы класса:<br/>

<b> - read(self, path) </b><br/>
        Читает содержимое файла, по адресу path <br/>
        Результат, разделённый по секциям,
        записывается в атрибут экземпляра класса self.query (dict)<br/>
        В формате <i>{section: query}</i> <br/>
        В .sql файле запросы записываются <ins>строго</ins> в формате:<br/>
        &nbsp&nbsp <i>--название_запроса</i><br/>
        &nbsp&nbsp <i>код запроса;</i><br/><br/>

<b> - has_section(self, section) </b><br/>
Проверяет наличие секции (запроса) <i>section</i> внутри прочитанного файла <br/><br/>

<b> - get_item(self, section) </b><br/>
        Возвращает параметры внутри секции <i>section</i> файла
        в виде строки<br/>

<h4>Модуль config, функция config</h4>
Для перевода параметров базы данных из секции <i>section</i> файла <i>filename</i><br/>
в словарь формата <i>{parameter: value}</i><br/>
По умолчанию <i>filename = src/database.ini, section = 'postgresql'</i><br/>
Используется модулем <b>database_fill</b> и <b>dbmanager</b>


<h3>4. Запросы к базе данных. Модули parser, config</h3>
<h4>Класс DBManager</h4>
Класс для взаимодействия с базой данных<br/>
Инициализирует внутри себя экземпляр класса QueryParser<br/>

Методы класса:<br/>

<b> - execute_query(query_name, query_params, params) </b><br/>
        Запускает в базе данных sql запрос из .sql файла, заданным парсером.<br/>
        Остальные методы для запросов используют этот метод<br/>
        Параметры метода:<br/>
        &nbsp &nbsp <i>query_name</i> - название запроса, согласно файлу queries.sql<br/>
        &nbsp &nbsp <i>query_params</i> - словарь параметров параметризованного запроса, при наличии параметров в запросе<br/>
        &nbsp &nbsp <i>params</i> - словарь параметров базы данных (по умолчанию из database.ini)<br/>
        Возращает кортеж из:<br/>
        &nbsp &nbsp - список названий колонок<br/>
        &nbsp &nbsp - список кортежей строк<br/>
    
<b> - get_vacancies_with_keyword(self, keyword, params=config()) </b><br/>
        Переводит результат execute_query из формата
        список кортежей <i>[(value, value, ...)]</i><br/>
        в формат списка словарей <i>[{colname: value}]</i>

<b>Все следующие методы используют параметр config, по умолчанию берётся из модуля config<br/>
Возвращают результат в виде списка словарей <i>[{colname: value}]</i></b><br/><br/>
<b> - get_companies_and_vacancies_count(self, params=config()) </b><br/>
    получает список всех компаний и количество вакансий у каждой компании <br/>

<b> - get_all_vacancies(self, params=config()) </b><br/>
        получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию. <br/><br/>

<b> - get_avg_salary(self, params=config()) </b><br/>
        получает среднюю зарплату по вакансиям. <br/><br/>

<b> - get_vacancies_with_higher_salary(self, params=config()) </b><br/>
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. <br/><br/>

<b> - get_vacancies_with_keyword(self, keyword, params=config()) </b><br/>
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. <br/><br/>