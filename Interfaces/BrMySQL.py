#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Sensor information are in the MySQL database in lab.
"""
import mysql.connector as mc


class ConnMySQL(object):

    def __init__(self, database, user, password, host, port, **kwargs):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.othersetting = kwargs
        self.conn = mc.connect(host=self.host, port=self.port,
                               user=self.user, password=self.password)
        self.conn.autocommit = True
        self.cur = self.conn.cursor(buffered=True)
        # charset = "utf8mb4"
        # self.charset = charset

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print('\nSQL Error Type : {}\n'
                  '--- Error Value: {}\n'
                  '--- Error is at: {}'.format(exc_type, exc_val, exc_tb))
        self.close()

    def select_db(self, db):
        try:
            self.conn.select_db(db)
        except mc.Error as e:
            print("Mysql Error {:d}: {}".format(e.args[0], e.args[1]))

    def query(self, sql):
        print("Executing SQL script:\n  '{}'".format(sql))
        try:
            n = self.cur.execute(sql)
            return n
        except mc.Error as e:
            print("MySQL Error: {}\n  with SQL: '{}'".format(e, sql))

    def fetch(self, fetch_type, with_description=False):
        if fetch_type is 'ALL':
            return self.fetch_all(with_description)  # return a list of tuples: [(),(),...]
        else:
            return self.fetch_row(with_description)  # return a tuple

    def fetch_row(self, with_description=False):
        result = self.cur.fetchone()
        if with_description:
            col_name = [i[0] for i in self.cur.describe]
            return dict((col, res) for col, res in zip(col_name, result))
        else:
            return result

    def fetch_all(self, with_description=False):
        result = self.cur.fetchall()  # a list of tuples
        col_name = [i[0] for i in self.cur.describe]  # cur.describe[0] = column name
        if with_description:
            d = []
            for oneline in result:
                d.append(dict((col, res) for col, res in zip(col_name, oneline)))
            return d
        else:
            return result

    def have_a_look(self, db_name, table_name):
        _sql = 'select * from {}.{} '.format(db_name, table_name)
        self.query(_sql)
        _result = self.fetch_all()
        for row in _result:
            print(row)

    def select(self, id_name, key_id, db_name, table_name, *col_name):
        _sql = 'select {} from {}.{} where {}={}' \
            .format(', '.join(col_name), db_name, table_name, id_name, key_id)
        print("Executing SQL script:\n  '{}'".format(_sql))
        self.query(_sql)

    def insert(self, table_name, data):
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `', table_name, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s"] * len(columns))
        # _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
        _params = [data[key] for key in columns]
        return self.cur.execute(_sql, tuple(_params))

    def update(self, tbname, data, condition):
        _fields = []
        _prefix = "".join(['UPDATE `', tbname, '`', 'SET'])
        for key in data.keys():
            _fields.append("%s = %s" % (key, data[key]))
        _sql = "".join([_prefix, _fields, "WHERE", condition])

        return self.cur.execute(_sql)

    def delete(self, tbname, condition):
        _prefix = "".join(['DELETE FROM  `', tbname, '`', 'WHERE'])
        _sql = "".join([_prefix, condition])
        return self.cur.execute(_sql)

    def get_last_insert_id(self):
        return self.cur.lastrowid

    def rowcount(self):
        return self.cur.rowcount

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()

    @property
    def backup_path(self):
        if 'path' in self.othersetting.keys():
            return self.othersetting['path']
        else:
            return 'No backup file path is provided for {}'.format(self)
