import psycopg2
import pymysql
from pymongo import MongoClient

from config import POSTGRES, MYSQL, MONGO


def postgres_conn():
    return psycopg2.connect(**POSTGRES)


def mysql_conn():
    return pymysql.connect(
        host=MYSQL["host"],
        port=MYSQL["port"],
        user=MYSQL["user"],
        password=MYSQL["password"],
        database=MYSQL["database"],
        local_infile=True,
        autocommit=False,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.Cursor,
    )


def mongo_client():
    return MongoClient(MONGO["uri"])


def mongo_collection():
    client = mongo_client()
    return client[MONGO["database"]][MONGO["collection"]]
