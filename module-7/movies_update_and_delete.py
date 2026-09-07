"""CSD 310 Module 7.2: Insert, update, and delete movie records."""

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values


def show_films(cursor, title):
    """Display each film with its director, genre, and studio."""
    query = (
        "SELECT film.film_name AS Name, "
        "film.film_director AS Director, "
        "genre.genre_name AS Genre, "
        "studio.studio_name AS Studio "
        "FROM film "
        "INNER JOIN genre ON film.genre_id = genre.genre_id "
        "INNER JOIN studio ON film.studio_id = studio.studio_id "
        "ORDER BY film.film_id"
    )

    cursor.execute(query)
    films = cursor.fetchall()

    print(f"\n-- {title} --")
    for film in films:
        print(f"Name: {film[0]}")
        print(f"Director: {film[1]}")
        print(f"Genre: {film[2]}")
        print(f"Studio: {film[3]}\n")


def main():
    """Connect to MySQL and complete the required database changes."""
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

        show_films(cursor, "DISPLAYING FILMS")

        insert_query = (
            "INSERT INTO film "
            "(film_name, film_releaseDate, film_runtime, film_director, "
            "studio_id, genre_id) "
            "VALUES (%s, %s, %s, %s, "
            "(SELECT studio_id FROM studio WHERE studio_name = %s), "
            "(SELECT genre_id FROM genre WHERE genre_name = %s))"
        )
        new_film = (
            "Nope",
            "2022",
            130,
            "Jordan Peele",
            "Universal Pictures",
            "Horror",
        )
        cursor.execute(insert_query, new_film)
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

        update_query = (
            "UPDATE film "
            "SET genre_id = "
            "(SELECT genre_id FROM genre WHERE genre_name = %s) "
            "WHERE film_name = %s"
        )
        cursor.execute(update_query, ("Horror", "Alien"))
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

        delete_query = "DELETE FROM film WHERE film_name = %s"
        cursor.execute(delete_query, ("Gladiator",))
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

        cursor.close()

    except mysql.connector.Error as err:
        if db is not None:
            db.rollback()

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
