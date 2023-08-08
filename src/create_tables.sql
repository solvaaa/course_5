-- создание таблицы employers
CREATE TABLE employers (
    employer_id INT PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    url VARCHAR(50),
    description TEXT
);

-- создание таблицы vacancies
CREATE TABLE vacancies (
    vacancy_id INT PRIMARY KEY NOT NULL,
    employer_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    url VARCHAR(50),
    salary_from INT,
    salary_to INT,
    description TEXT
);

--создание внешнего ключа employer_id в таблице vacancies
ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employers
    FOREIGN KEY(employer_id) REFERENCES employers(employer_id);

