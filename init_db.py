import os
import psycopg2


def get_conn():
    conn = psycopg2.connect(
            host='',
            database="",
            user='',
            password='')
    return conn
