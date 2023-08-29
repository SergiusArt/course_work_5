import psycopg2


class DBWork:

    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        """
        Инициализация класса
        """

        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

        self.conn = None
        self.cur = None

    def connect(self):
        """
        Подключение к базе данных
        """

        try:
            self.conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            self.cur = self.conn.cursor()
            print("Connected to database")
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        """
        Отключение от базы данных
        """

        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Disconnected from database")

    def create_tables(self):
        """
        Создание таблиц
        """

        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id char(100) PRIMARY KEY,
                    name text,
                    vacancies_count INTEGER
                )
            """)

            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id char(100) PRIMARY KEY,
                    company_id text,
                    name text,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency text,
                    url text
                    
                )
            """)
            # FOREIGN KEY (company_id) REFERENCES companies (id)
            self.conn.commit()
            print("Tables created")
        except psycopg2.Error as e:
            print(f"Error creating tables: {e}")

    def insert_company(self, company_id, name, vacancies_count):
        """
        Наполнение данных таблицы company
        """

        try:
            self.cur.execute("""
                INSERT INTO companies (id, name, vacancies_count)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (company_id, name, vacancies_count))
            self.conn.commit()
            print(f"Company inserted with id: {company_id}")
            return company_id
        except psycopg2.Error as e:
            print(f"Error inserting company: {e}")
            return None

    def insert_vacancy(self, vacancy_id, company_id, name, currency, salary_from, salary_to, url):
        """
        Наполнение данных таблицы vacancy
        """

        try:
            self.cur.execute("""
                INSERT INTO vacancies (id, company_id, name, salary_from, salary_to, currency, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (vacancy_id, company_id, name, salary_from, salary_to, currency, url))
            self.conn.commit()
            print(f"Vacancy inserted with id: {vacancy_id}")
            return vacancy_id
        except psycopg2.Error as e:
            print(f"Error inserting vacancy: {e}")
            return None
