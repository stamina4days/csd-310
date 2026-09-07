"""CSD 310 Module 6.2: Query the movies database."""

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values


def print_studios(cursor):
    """Display every record from the studio table."""
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    studios = cursor.fetchall()

    print("\n-- DISPLAYING Studio RECORDS --")
    for studio in studios:
        print(f"Studio ID: {studio[0]}")
        print(f"Studio Name: {studio[1]}\n")


def print_genres(cursor):
    """Display every record from the genre table."""
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    genres = cursor.fetchall()

    print("-- DISPLAYING Genre RECORDS --")
    for genre in genres:
        print(f"Genre ID: {genre[0]}")
        print(f"Genre Name: {genre[1]}\n")


def print_short_films(cursor):
    """Display films with a runtime of less than two hours."""
    cursor.execute(
        "SELECT film_name, film_runtime "
        "FROM film "
        "WHERE film_runtime < 120"
    )
    films = cursor.fetchall()

    print("-- DISPLAYING Short Film RECORDS --")
    for film in films:
        print(f"Film Name: {film[0]}")
        print(f"Runtime: {film[1]} minutes\n")


def print_films_by_director(cursor):
    """Display every film with films from the same director together."""
    cursor.execute(
        "SELECT film_name, film_director "
        "FROM film "
        "ORDER BY film_director, film_name"
    )
    films = cursor.fetchall()

    print("-- DISPLAYING Director RECORDS in Order --")
    for film in films:
        print(f"Film Name: {film[0]}")
        print(f"Director: {film[1]}\n")


def main():
    """Connect to MySQL, run the four queries, and close the connection."""
    secrets = dotenv_values(".env")
    config = {
        "user": secrets["USER"],
        "password": secrets["PASSWORD"],
        "host": secrets["HOST"],
        "database": secrets["DATABASE"],
        "raise_on_warnings": True,
    }

    db = None

    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        print_studios(cursor)
        print_genres(cursor)
        print_short_films(cursor)
        print_films_by_director(cursor)

        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The supplied username or password is invalid.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The specified database does not exist.")
        else:
            print(err)

    finally:
        if db is not None and db.is_connected():
            db.close()


if __name__ == "__main__":
    main()
