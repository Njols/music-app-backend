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


def main(req: func.HttpRequest) -> func.HttpResponse:
    conn = connect()
    cursor = conn.cursor()
    group_id = req.params.get("group_id")
    if req.method == "GET":
        cursor.execute(
            """
        SELECT * FROM posts WHERE groupId = %(group_id)s
        """,
            {"group_id": group_id},
        )
        results = cursor.fetchall()
        posts = []
        for result in results:
            cursor.execute(
                """
                SELECT (userId, username) FROM users WHERE id = %(user_id_internal)s
                """,
                {"user_id_internal": result[3]},
            )
            user = cursor.fetchone()
            post = {
                "post_id": result[0],
                "title": result[1],
                "content": result[2],
                "user": {"user_id": user[0], "username": user[1]},
                "group_id": group_id,
            }
            posts.append(post)

        conn.close()
        return func.HttpResponse(body=json.dump(posts), status_code=200)

    if req.method == "POST":
        body = req.get_json()
        # Attempt to get the content, the user id and the title from the request body
        try:
            content = body["content"]
            user_id = body["user_id"]
            title = body["title"]
        except:
            conn.close()
            return func.HttpResponse(status_code=401)

        # Attempt to get the internal ids from the groups and users based on their external ids
        try:
            cursor.execute(
                """
                SELECT id FROM groups WHERE group_id = %(group_id)s 
                """,
                {"group_id": group_id},
            )
            group_id_internal = cursor.fetchone()
            cursor.execute(
                """
                SELECT id from users WHERE user_id = %(user_id)s
                """,
                {"user_id": user_id},
            )
            user_id_internal = cursor.fetchone()
        except:
            conn.close()
            return func.HttpResponse(status_code=404)

        # Execute the actual insert query
        cursor.execute(
            """
        INSERT INTO posts (group_id, content, user_id, title) VALUES (%(groupId)s, %(content)s, %(userId)s, %(title)s)        
        """,
            {
                "groupId": group_id_internal,
                "content": content,
                "userId": user_id_internal,
                "title": title,
            },
        )
        conn.commit()
        conn.close()
        return func.HttpResponse(status_code=201)
