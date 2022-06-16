import logging
import json
import mysql.connector
from mysql.connector import MySQLConnection, Error
import azure.functions as func
from configparser import ConfigParser


def read_db_config(filename="config.ini", section="mysql"):
    """Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception("{0} not found in the {1} file".format(section, filename))

    return db


def connect():
    """Connect to MySQL database"""

    db_config = read_db_config()
    conn = None
    try:
        print("Connecting to MySQL database...")
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print("Connection established.")
        else:
            print("Connection failed.")

    except Error as error:
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            return conn


def main(myQueueItem) -> None:
    conn = connect()
    cursor = conn.cursor()
    if myQueueItem.properties.content_type == "user_created":
        user = myQueueItem.body
        cursor.execute(
            """
            SELECT * FROM users WHERE userId = %(user_id)s
            """,
            {"user_id": user["user_id"]},
        )
        if not cursor.fetchone():
            cursor.execute(
                """
                INSERT INTO users (userId, username) VALUES (%(user_id)s, %(username)s)
                """,
                {"user_id": user["user_id"], "username": user["username"]},
            )
            conn.commit()

    if myQueueItem.properties.content_type == "user_deleted":
        data = myQueueItem.body
        cursor.execute(
            """
            SELECT * FROM users WHERE userId = %(user_id)s
            """,
            {"user_id": data},
        )
        user = cursor.fetchone()
        if user:
            cursor.execute(
                """
                DELETE FROM users WHERE userId = %(user_id)s
                """,
                {"user_id": data},
            )
            conn.commit()

    if myQueueItem.properties.content_type == "user_changed":
        new_user = myQueueItem.body
        cursor.execute(
            """
            SELECT * FROM users WHERE userId = %(user_id)s
            """,
            {"user_id": new_user["id"]},
        )
        user = cursor.fetchone()
        if user:
            cursor.execute(
                """
                UPDATE users SET userId = %(user_id)s, username %(username)s WHERE id = %(id)s
                """,
                {
                    "user_id": new_user["id"],
                    "username": new_user["username"],
                    "id": user[0],
                },
            )
            conn.commit()
    conn.close()
