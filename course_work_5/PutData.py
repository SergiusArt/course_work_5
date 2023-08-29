import requests


class PutData:

    def __init__(self):
        pass
        self.company_id = []
        self.company_name = []
        self.vacancies_count = []

        self.vacancies_id = []
        self.vacancies_company_id = []
        self.vacancies_name = []
        self.salary_from = []
        self.salary_to = []
        self.currency = []
        self.url = []

    def put_companies(self):
        """
        Формирует словари данных для таблицы с данными Companies
        """

        url = "https://api.hh.ru/employers"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data['items']:
                self.company_id.append(item['id'])
                self.company_name.append(item['name'])
                self.vacancies_count.append(item['open_vacancies'])
        else:
            print("Failed to retrieve data from API")

    def put_vacancies(self):
        """
        Формирует словари данных для таблицы с данными Vacancies
        """

        url = "https://api.hh.ru/vacancies"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data['items']:
                salary = item['salary']
                self.vacancies_id.append(item['id'])
                self.vacancies_company_id.append(item['employer']['name'])
                self.vacancies_name.append(item['name'])
                try:
                    self.url.append(item['apply_alternate_url'])
                except KeyError:
                    self.url.append('-')
                if salary:
                    if item['salary']['from']:
                        self.salary_from.append(item['salary']['from'])
                    else:
                        self.salary_from.append('0')
                    if item['salary']['to']:
                        self.salary_to.append(item['salary']['to'])
                    else:
                        self.salary_to.append('0')
                    self.currency.append(item['salary']['currency'])
                else:
                    self.salary_from.append('0')
                    self.salary_to.append('0')
                    self.currency.append('не указана')
        else:
            print("Failed to retrieve data from API")
