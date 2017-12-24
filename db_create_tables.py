import connection


class DBManager:
    def __init__(self):
        self.connection = connection.Connection(host="localhost", db_name="ask_db", user="'yury'",
                                                password="89096547567")

    def create_tables(self):
        with self.connection as c:
            cursor = c.cursor()
            cursor.execute("""drop table ask_app_question""")
            cursor.execute("""drop table ask_app_userprofile""")
            cursor.execute("""create table
                ask_app_question (
                id INT(11) NOT NULL AUTO_INCREMENT,
                title CHAR(100) NOT NULL,
                author_id INT,
                text TEXT,
                create_date DATE,
                likes INT,
                FOREIGN KEY (author_id) REFERENCES ask_app_userprofile(id),
                PRIMARY KEY(id)
                )""")
            cursor.execute("""create table
                ask_app_userprofile (
                id int(11) NOT NULL AUTO_INCREMENT,
                password varchar(128),
                last_login datetime(6),
                is_superuser tinyint(1),
                username varchar(150),
                first_name varchar(30),
                last_name varchar(30),
                email varchar(254),
                is_staff tinyint(1),
                is_active tinyint(1),
                date_joined datetime(6),
                PRIMARY KEY(id)
                )""")
            c.commit()

    def drop_tables(self):
        with self.connection as c:
            cursor = c.cursor()
            cursor.execute("""drop table ask_app_question""")
            cursor.execute("""drop table ask_app_userprofile""")
            c.commit()

    def create_table_question(self):
        with self.connection as c:
            cursor = c.cursor()
            cursor.execute("""create table
                ask_app_question (
                id INT(11) NOT NULL AUTO_INCREMENT,
                title CHAR(100) NOT NULL,
                author_id INT,
                text TEXT,
                create_date DATE,
                likes INT,
                FOREIGN KEY (author_id) REFERENCES ask_app_userprofile(id),
                PRIMARY KEY(id)
                )""")
            c.commit()

    def drop_table_question(self):
        with self.connection as c:
            cursor = c.cursor()
            cursor.execute("""drop table ask_app_question""")
            c.commit()

    def create_table_userprofile(self):
        with self.connection as c:
            cursor = c.cursor()
            cursor.execute("""create table
                            ask_app_userprofile (
                            id int(11) NOT NULL AUTO_INCREMENT,
                            password varchar(128),
                            last_login datetime(6),
                            is_superuser tinyint(1),
                            username varchar(150),
                            first_name varchar(30),
                            last_name varchar(30),
                            email varchar(254),
                            is_staff tinyint(1),
                            is_active tinyint(1),
                            date_joined datetime(6),
                            PRIMARY KEY(id)
                            )""")
            c.commit()


dbManager = DBManager()

# needed for first start of program
# dbManager.drop_tables()
# dbManager.create_tables()

dbManager.drop_tables()
#dbManager.create_table_userprofile()
#dbManager.create_table_question()
