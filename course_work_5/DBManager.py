import psycopg2
import os


class DBManager:
    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """

        conn = psycopg2.connect(
            dbname='hh',
            user='postgres',
            password=os.getenv('DB_Password'),
            host='localhost',
            port='5432'
        )

        cursor = conn.cursor()

        # Получаем список компаний и количество вакансий у каждой компании
        query = """
                SELECT name, vacancies_count
                FROM companies
            """
        cursor.execute(query)
        results = cursor.fetchall()

        # Создаем словарь с результатами
        company_vacancies = {}
        for result in results:
            company_name = result[0]
            vacancies_count = result[1]
            company_vacancies[company_name] = vacancies_count

        cursor.close()
        conn.close()

        return company_vacancies

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """

        conn = psycopg2.connect(
            dbname='hh',
            user='postgres',
            password=os.getenv('DB_Password'),
            host='localhost',
            port='5432'
        )

        cursor = conn.cursor()

        # Получаем список компаний и количество вакансий у каждой компании
        query = """
                SELECT id, company_id, name, salary_from, salary_to, currency, url
                FROM vacancies
            """
        cursor.execute(query)
        results = cursor.fetchall()

        # Создаем словарь с результатами
        vacancies = {}
        for result in results:
            vacancies[result[0]] = [result[1], result[2], result[3], result[4], result[5], result[6]]

        cursor.close()
        conn.close()

        return vacancies

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """

        conn = psycopg2.connect(
            dbname='hh',
            user='postgres',
            password=os.getenv('DB_Password'),
            host='localhost',
            port='5432'
        )

        cursor = conn.cursor()

        # Получаем список компаний и количество вакансий у каждой компании
        query = """
                SELECT name, AVG((salary_from + salary_to) / 2) as avg_salary, currency
                FROM vacancies
                GROUP BY name, currency
            """
        cursor.execute(query)
        results = cursor.fetchall()

        # Создаем словарь с результатами
        avg_salary = {}
        for result in results:
            avg_salary[result[0]] = [result[1], result[2]]

        cursor.close()
        conn.close()

        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """

        conn = psycopg2.connect(
            dbname='hh',
            user='postgres',
            password=os.getenv('DB_Password'),
            host='localhost',
            port='5432'
        )

        cursor = conn.cursor()

        # Получаем список компаний и количество вакансий у каждой компании
        query = """
                SELECT name, (salary_from + salary_to) / 2, currency
                FROM vacancies
                WHERE (salary_from + salary_to) / 2 > (
                  SELECT AVG((salary_from + salary_to) / 2)
                  FROM vacancies
                )
            """
        cursor.execute(query)
        results = cursor.fetchall()

        # Создаем словарь с результатами
        vacancies_with_higher_salary = {}
        for result in results:
            vacancies_with_higher_salary[result[0]] = [result[1], result[2]]

        cursor.close()
        conn.close()

        return vacancies_with_higher_salary

    def get_vacancies_with_keyword(self, key_word):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """

        conn = psycopg2.connect(
            dbname='hh',
            user='postgres',
            password=os.getenv('DB_Password'),
            host='localhost',
            port='5432'
        )

        cursor = conn.cursor()

        # Получаем список компаний и количество вакансий у каждой компании
        query = f"SELECT id, company_id, name, salary_from, salary_to, currency, url " \
                f"FROM vacancies " \
                f"WHERE name LIKE '%{key_word.lower()}%' or name LIKE '%{key_word.capitalize()}%'"
        cursor.execute(query)
        results = cursor.fetchall()

        # Создаем словарь с результатами
        vacancies_with_keyword = {}
        for result in results:
            vacancies_with_keyword[result[0]] = [result[1], result[2], result[3], result[4], result[5], result[6]]

        cursor.close()
        conn.close()

        return vacancies_with_keyword
