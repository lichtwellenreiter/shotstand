import sqlite3


class Database:

    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.conn.execute("CREATE TABLE IF NOT EXISTS shotmeter (" \
                          "id INTEGER PRIMARY KEY, " \
                          "groupname TEXT not null , " \
                          "shotcount INTEGER," \
                          "CONSTRAINT groupname_uq UNIQUE (groupname))")

    def add_entry(self, groupname, shots):
        cur = self.conn.cursor()
        sql = "SELECT * FROM shotmeter where groupname = '{groupname}' LIMIT 1".format(groupname=groupname)
        cur.execute(sql)

        print(sql)

        rows = cur.fetchall()
        print(len(rows))
        print(rows)

        if len(rows) > 0:
            newshots = rows[0][2] + int(shots)
            print(newshots)
            sql = "UPDATE shotmeter set shotcount = {shotcount} where groupname = '{groupname}'".format(
                shotcount=newshots,
                groupname=groupname)
        else:
            sql = "INSERT INTO shotmeter ('groupname', 'shotcount') VALUES ('{groupname}', {shotcount})".format(
                groupname=groupname, shotcount=shots)

        self.conn.execute(sql)
        self.conn.commit()

    def get_grounames(self):
        sql = "select groupname from shotmeter"
        rows = self.conn.execute(sql)
        names = []
        for name in rows:
            print(name)
            names.append(name[0])
        return names

    def get_group_shots(self):
        sql = "select * from shotmeter order by shotcount desc"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        print(rows)
        return rows
