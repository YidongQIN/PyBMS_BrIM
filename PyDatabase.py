#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
BrIM should use database to store the information of elements, 
structural members or non-structural members, such as sensor, etc.
not only MySQL, but also NoSQL later.
"""

import mysql.connector as mc


class ConnMySQL(object):

    def __init__(self, host, database, user, password, port, charset="utf8"):
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        try:
            self.conn = mc.connect(host=self.host, port=self.port,
                                   user=self.user, password=self.password)
            # self.conn.autocommit(False)
            # self.conn.set_character_set(self.charset)
            # self.cur = self.conn.cursor()
            #buffered, or may have error: 'mysql.connector.errors.InternalError: Unread result found'
            self.cur = self.conn.cursor(buffered=True)
        except mc.Error as e:
            print("Mysql Error {:d}: {}".format(e.args[0], e.args[1]))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print('SQL Error Type: {}\n'
                  '----ErrorValue: {}\n'
                  '----Error TB: {}'.format(exc_type, exc_val, exc_tb))
        self.close()

    # def __del__(self):
    #     self.close()

    def select_db(self, db):
        try:
            self.conn.select_db(db)
        except mc.Error as e:
            print("Mysql Error {:d}: {}".format(e.args[0], e.args[1]))

    def query(self, sql):
        try:
            n = self.cur.execute(sql)
            return n
        except mc.Error as e:
            print("Mysql Error:{}\nSQL:{}".format(e, sql))

    def fetch_row(self, with_description=False):
        result = self.cur.fetchone()
        if with_description:
            col_name = [i[0] for i in self.cur.description]
            return dict((col, res) for col, res in zip(col_name, result))
        else:
            return result


    def fetch_all(self, with_description=False):
        result = self.cur.fetchall()  # a list of tuples
        col_name = [i[0] for i in self.cur.description]
        # cur.description[0] is the column name
        d = []
        if with_description:
            for oneline in result:
                d.append(dict((col, res) for col, res in zip(col_name, oneline)))
            return d
        else:
            return result

    def insert(self, table_name, data):
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `', table_name, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s"]* len(columns))
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
