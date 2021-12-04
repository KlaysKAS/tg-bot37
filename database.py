import psycopg2


class DB(object):
    def __init__(self, url):
        self.conn = psycopg2.connect(url, sslmode='require')
        self.__checkMigrationAndMigrate()

    def dropAllTables(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE registration")
        cur.execute("DROP TABLE users")
        cur.execute("DROP TABLE migrations")
        cur.close()
        self.conn.commit()

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

    version = 2
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
    ]

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
