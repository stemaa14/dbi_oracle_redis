import cx_Oracle as orcl
import sys

conn = None


def connect():
    global conn
    if conn:
        conn.close()
    conn = orcl.connect('stemaa14/stemaa14@db2.htl-kaindorf.at/orcl')


def transaction(func):
    def wrapper(obj):
        attempt = 0
        while attempt <= 3:
            try:
                attempt += 1
                return func(obj)
            except Exception as e:
                print >> sys.stderr, e
                connect()
    return wrapper


connect()
