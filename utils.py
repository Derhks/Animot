import psycopg2
import requests

from config import config


def get(url: str) -> dict:
    try:
        response = requests.get(url=url)

    except requests.exceptions.HTTPError as Err:
        raise Err

    return response.json()


def postgres_execute(*args) -> None:
    """
    Connect to the PostgreSQL database server and run the
    command on the database
    """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # insert info
        cur.execute(*args)

        # close the communication with the PostgreSQL
        cur.close()

        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        raise error
    finally:
        if conn is not None:
            conn.close()
