import os
import psycopg2


def get_conn():
    conn = psycopg2.connect(
            host='ec2-34-247-72-29.eu-west-1.compute.amazonaws.com',
            database="d466as9buoni53",
            user='rzrcatwrsoxksq',
            password='512ffb9447de5be9e3b0ffe93d9541bc0d4ee3ccdecc289f3e8112a4c0741bec')
    return conn