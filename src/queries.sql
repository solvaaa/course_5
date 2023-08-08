--Все запросы в формате:
--Название
--Запрос;
--get_companies_and_vacancies_count
SELECT employers.name, COUNT(vacancy_id) AS num_of_vacancies
FROM employers
JOIN vacancies USING(employer_id)
GROUP BY employers.name;

--get_all_vacancies
SELECT
	employers.name,
	vacancies.name,
	salary_from,
	salary_to,
	vacancies.url
FROM employers
JOIN vacancies USING(employer_id);

--get_avg_salary
SELECT
	ROUND(AVG(salary_from)) AS average_salary
FROM vacancies;

--get_vacancies_with_higher_salary
SELECT *
FROM vacancies
WHERE salary_from > (
	SELECT AVG(salary_from)
	FROM vacancies)
ORDER BY salary_from DESC;

--get_vacancies_with_keyword
SELECT *
FROM vacancies
WHERE LOWER(name) LIKE %(keyword)s
