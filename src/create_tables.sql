CREATE TABLE employers (
    employer_id INT PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    url VARCHAR(50),
    description TEXT
);

CREATE TABLE vacancies (
    vacancy_id INT PRIMARY KEY NOT NULL,
    employer_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    url VARCHAR(50),
    salary_from INT,
    salary_to INT,
    description TEXT
);

