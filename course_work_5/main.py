from PutData import PutData
from DB_work import DBWork
from DBManager import DBManager
import os


def new_db():
    """
    Создание новой базы данных
    """

    # Параметры для подключения к БД
    host = 'localhost'
    database = 'hh'
    user = 'postgres'
    port = '5432'
    password = os.getenv('DB_Password')
    # Создание объекта для загрузки данных в БД
    hh_data = PutData()

    # Подключение к базе данных
    DB_hh = DBWork(db_host=host, db_port=port, db_name=database, db_user=user, db_password=password)

    # Открытие базы данных
    DB_hh.connect()

    # Создание таблиц
    DB_hh.create_tables()

    # Добавление данных о компаниях
    hh_data.put_companies()
    for i in range(len(hh_data.company_name)):
        DB_hh.insert_company(company_id=hh_data.company_id[i],
                             name=hh_data.company_name[i],
                             vacancies_count=hh_data.vacancies_count[i]
                             )
    # Добавление данных о вакансиях
    hh_data.put_vacancies()
    for i in range(len(hh_data.vacancies_id)):
        DB_hh.insert_vacancy(vacancy_id=hh_data.vacancies_id[i],
                             company_id=hh_data.vacancies_company_id[i],
                             name=hh_data.vacancies_name[i],
                             salary_from=hh_data.salary_from[i],
                             salary_to=hh_data.salary_to[i],
                             currency=hh_data.currency[i],
                             url=hh_data.url[i]
                             )
    # Закрытие базы данных
    DB_hh.disconnect()


def dialog():
    """
    Выбор пункта меню пользователем
    """

    try:
        choice = int(input('Выберите нужное действие:\n'
                           '1: Получить список всех компаний и количество вакансий у каждой компании\n'
                           '2: Получить список всех вакансий с указанием названия компании названия вакансии'
                           ' и зарплаты и ссылку на вакансию\n'
                           '3: Получить среднюю зарплату по вакансиям\n'
                           '4: Получить список всех вакансий у которых зарплата выше средней по всем вакансиям\n'
                           '5: Получить список всех вакансий в названии которых содержатся указанные слова,'
                           ' например: python\n'
                           '--> '))
        if choice in range(6):
            if choice == 1:
                for key, item in manager_db.get_companies_and_vacancies_count().items():
                    print(f'Компания: {key}, Количество вакансий: {item}')

            elif choice == 2:
                for key, item in manager_db.get_all_vacancies().items():
                    word_from = ' от '
                    word_to = ' до '
                    if item[2] == 0:
                        item[2] = ''
                        word_from = ''
                    if item[3] == 0:
                        item[3] = ''
                        word_to = ''
                    print(f'Компания: {item[0]}, вакансия: {item[1]}, зарплата:'
                          f'{word_from}{item[2]}{word_to}{item[3]} {item[4]}, ссылка: {item[5]}')

            elif choice == 3:
                for key, item in manager_db.get_avg_salary().items():
                    if int(item[0]) == 0:
                        print(f'Вакансия: {key}, Средняя зарплата: {item[1]}')
                    else:
                        print(f'Вакансия: {key}, Средняя зарплата: {int(item[0])} {item[1]}')

            elif choice == 4:
                for key, item in manager_db.get_vacancies_with_higher_salary().items():
                    if int(item[0]) == 0:
                        print(f'Вакансия: {key}, Средняя зарплата: {item[1]}')
                    else:
                        print(f'Вакансия: {key}, Средняя зарплата: {int(item[0])} {item[1]}')

            elif choice == 5:
                key_word = input('Введите ключевое слово для поиска -> ')
                for key, item in manager_db.get_vacancies_with_keyword(key_word).items():
                    word_from = ' от '
                    word_to = ' до '
                    if item[2] == 0:
                        item[2] = ''
                        word_from = ''
                    if item[3] == 0:
                        item[3] = ''
                        word_to = ''
                    print(
                        f'Компания: {item[0]}, вакансия: {item[1]}, зарплата:'
                        f'{word_from}{item[2]}{word_to}{item[3]} {item[4]}, ссылка: {item[5]}')
        else:
            print('Не верно выбрано действие')
    except ValueError as e:
        print(f'Не верно выбрано действие: {e}')


# Создание новой базы данных
new_db()

manager_db = DBManager()

# Создание диалога с пользователем
dialog()
