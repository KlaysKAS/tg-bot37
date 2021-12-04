import psycopg2


class DB(object):
    def __init__(self, url):
        self.conn = psycopg2.connect(url, sslmode='require')

    def migration0_1(self):
        TODO("INIT MIGRATION")
