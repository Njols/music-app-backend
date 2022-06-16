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
    if myQueueItem.properties.content_type == "group_created":
        group = myQueueItem.body
        cursor.execute(
            """
            SELECT * FROM groups WHERE groupId = %(group_id)s
            """,
            {"group_id": group["id"]},
        )
        if not cursor.fetchone():
            cursor.execute(
                """
                INSERT INTO groups (groupId) VALUES (%(group_id)s)
                """,
                {"group_id": group["id"]},
            )
            conn.commit()

    if myQueueItem.properties.content_type == "group_deleted":
        group_id = myQueueItem.body
        cursor.execute(
            """
            SELECT * FROM groups WHERE groupId = %(group_id)s
            """,
            {"group_id": group_id},
        )
        if cursor.fetchone():
            cursor.execute(
                """
                DELETE FROM groups WHERE groupId = %(group_id)s
                """,
                {"group_id": group_id},
            )
            conn.commit()

    if myQueueItem.properties.content_type == "group_changed":
        new_group = myQueueItem.body
        cursor.execute(
            """
            SELECT * FROM groups WHERE groupId = %(group_id)s
            """,
            {"group_id": new_group["id"]},
        )
        group = cursor.fetchone()
        if group:
            cursor.execute(
                """
                UPDATE groups SET group_id = %(group_id)s WHERE id = %(id)s
                """,
                {"group_id": new_group["id"], "id": group[0]},
            )
            conn.commit()
    conn.close()
