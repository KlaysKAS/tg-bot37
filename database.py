import psycopg2


class DB(object):
    def __init__(self, url):
        self.conn = psycopg2.connect(url, sslmode='require')
        self.__checkMigrationAndMigrate()

    """Проверяет, если ли пользователь с заданной почтой среди людей, которые должны пройти курсы"""
    def checkUser(self, email):
        cur = 0
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = '{}' LIMIT 1".format(email))
            is_exist = cur.fetchall()
            return is_exist
        except (Exception, psycopg2.Error) as error:
            print("Check user is failed", error)
            if cur:
                cur.close()

    """Добавляет пользователя в таблицу пользователей, которые могут проходить курс
        users = [{
            'email': *user's email*
        }]
    """
    def addUsers(self, users):
        cur = 0
        try:
            cur = self.conn.cursor()
            for user in users:
                cur.execute("INSERT INTO users (email) VALUES ('{}')".format(user['email']))
            cur.close()
            self.conn.commit()
            return True
        except (Exception, psycopg2.Error) as error:
            print("Insert users is failed", error)
            if cur:
                cur.close()
        return False

    """Регистрирует пользователя на прохождение курса, если ему разрешен доступ
        course: banks, passwords, social_networking
    """
    def registerUser(self, email, course):
        cur = 0
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id FROM users WHERE email = '{}' LIMIT 1".format(email))
            res = cur.fetchall()
            if res:
                cur.execute("SELECT * FROM registration WHERE user_id = '{}'".format(res[0][0]))
                is_exist = cur.fetchall()
                if is_exist:
                    cur.execute("UPDATE registration SET {} = 'true' WHERE user_id = '{}'".format(course, res[0][0]))
                else:
                    cur.execute("INSERT INTO registration (user_id, {}) VALUES ({}, 'true')".format(course, res[0][0]))
                cur.close()
                self.conn.commit()
                return True
            else:
                print("User is not exist")
        except (Exception, psycopg2.Error) as error:
            print("Registration is failed", error)
            if cur:
                cur.close()
        return False

    """Записывает пользователя как admin'а, если у него есть доступ к курсу"""
    def setAdmin(self, email):
        cur = 0
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id FROM users WHERE email = '{}' LIMIT 1".format(email))
            res = cur.fetchall()
            if res:
                cur.execute("SELECT * FROM admins WHERE admin_id = '{}' LIMIT 1".format(res[0][0]))
                is_exist = cur.fetchall()
                if not is_exist:
                    cur.execute("INSERT INTO admins VALUES ({})".format(res[0][0]))
                cur.close()
                self.conn.commit()
                return True
            else:
                print("User is not exist")
        except (Exception, psycopg2.Error) as error:
            print("Admin set is failed", error)
        if cur:
            cur.close()
        return False

    """Проверяет, является ли пользователь admin'ом"""
    def checkAdmin(self, email):
        cur = 0
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id FROM users WHERE email = '{}' LIMIT 1".format(email))
            res = cur.fetchall()
            if res:
                cur.execute("SELECT * FROM admins WHERE admin_id = '{}' LIMIT 1".format(res[0][0]))
                is_exist = cur.fetchall()
                if is_exist:
                    return True
        except (Exception, psycopg2.Error) as error:
            print("Admin check is failed", error)
        if cur:
            cur.close()
        return False

    version = 3
    migrations = [
        [
            "CREATE TABLE users (" +
            "id SERIAL PRIMARY KEY, " +
            "full_name VARCHAR(200), " +
            "email VARCHAR(150) UNIQUE NOT NULL, " +
            "result SMALLINT" +
            ")",
            "CREATE TABLE registration (" +
            "user_id SERIAL NOT NULL, " +
            "email BOOLEAN DEFAULT 'false', " +
            "passwords BOOLEAN DEFAULT 'false', " +
            "social_networking BOOLEAN DEFAULT 'false', " +
            "FOREIGN KEY (user_id) REFERENCES users(id)" +
            ")"
        ],
        [
            "CREATE TABLE admins (" +
            "admin_id SERIAL UNIQUE NOT NULL, " +
            "FOREIGN KEY (admin_id) REFERENCES users(id))"
        ],
        [
            "ALTER TABLE registration RENAME COLUMN " +
            "email TO banks"
        ]
    ]

    def __checkMigrationAndMigrate(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='migrations'")
        migrations_is_created = cur.fetchall()
        cur.close()
        version = 0
        if not migrations_is_created:
            cur = self.conn.cursor()
            cur.execute("CREATE TABLE migrations (migrate INT NOT NULL)")
            cur.execute("INSERT INTO migrations VALUES (0)")
            cur.close()
            self.conn.commit()
        else:
            cur = self.conn.cursor()
            cur.execute("SELECT migrate FROM migrations")
            v = cur.fetchall()
            version = v[len(v) - 1][0]
            cur.close()
        cur = self.conn.cursor()
        while version < self.version:
            commands = self.migrations[version]
            for i in commands:
                cur.execute(i)
            version += 1
            cur.execute("INSERT INTO migrations VALUES ({})".format(version))
        cur.close()
        self.conn.commit()

    def dropUsers(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE users")
        cur.close()
        self.conn.commit()

    def dropAdmins(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE admins")
        cur.close()
        self.conn.commit()

    def dropAllTables(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE registration")
        cur.execute("DROP TABLE users")
        cur.execute("DROP TABLE migrations")
        cur.close()
        self.conn.commit()
