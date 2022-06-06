import sqlite3
import getopt
import sys
import os


class SQLiteDatabase:
    def __init__(self, dbname, path=None):
        if path:
            dbname = path + dbname
        self.db_conn = None
        self.create_database(dbname)

    def create_database(self, dbname):
        """ creates a new sqlite database """
        conn = None
        try:
            conn = sqlite3.connect(dbname)
            print(sqlite3.version)
        except sqlite3.Error as e:
            print(e)
        self.db_conn = conn

    def create_table(self, statement):
        try:
            c = self.db_conn.cursor()
            c.execute(statement)
        except sqlite3.Error as e:
            print(e)

    def insert_author(self, author_name):
        check = self.query_author_by_name(author_name)
        if check:
            return_id = check[0][0]
        else:
            cur = self.db_conn.cursor()
            sql = ''' INSERT INTO authors(fullname)
                      VALUES(?) '''
            cur.execute(sql, author_name)
            self.db_conn.commit()
            return_id = cur.lastrowid
        return return_id

    def query_author_by_name(self, author_name):
        cur = self.db_conn.cursor()
        sql = "SELECT * FROM authors WHERE fullname=?"
        cur.execute(sql, (author_name,))
        return cur.fetchone()

    def query_author_by_id(self, author_id):
        cur = self.db_conn.cursor()
        sql = "SELECT * FROM authors WHERE id=?"
        cur.execute(sql, (author_id,))
        return cur.fetchone()

    def insert_book(self, book_details):
        cur = self.db_conn.cursor()
        sql = ''' INSERT INTO books(title, author_id, book_path)
                  VALUES(?,?,?) '''
        cur.execute(sql, book_details)
        self.db_conn.commit()
        return cur.lastrowid

    def query_book_by_name(self, book_name, author_id):
        cur = self.db_conn.cursor()
        sql = "SELECT * FROM books WHERE title=? and author_id=?"
        cur.execute(sql, (book_name, author_id))
        return cur.fetchone()

    def get_all_authors(self):
        cur = self.db_conn.cursor()
        sql = "SELECT * from authors"
        cur.execute(sql)
        return cur.fetchall()

    def close_database(self):
        self.db_conn.close()


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:")
    except getopt.GetoptError:
        print('Usage: db_setup.py -d <database_file>')
        sys.exit(2)
    db_arg = 'default.db'
    for opt, arg in opts:
        if opt == '-d':
            db_arg = arg
    my_db = SQLiteDatabase(db_arg)

    sql_create_authors = """ CREATE TABLE IF NOT EXISTS authors (
                                id integer PRIMARY KEY,
                                fullname text NOT NULL
                              ); """

    sql_create_books = """ CREATE TABLE IF NOT EXISTS books (
                                id integer PRIMARY KEY,
                                title text NOT NULL,
                                author_id integer NOT NULL,
                                word_count integer,
                                avg_chapter_length real,
                                percent_speech real,
                                percent_rare_words real,
                                book_path text NOT NULL,
                                standard_deviation real,
                                FOREIGN KEY (author_id) REFERENCES authors (id)
                            );"""

    my_db.create_table(sql_create_authors)
    my_db.create_table(sql_create_books)

    sql_create_categories = """ CREATE TABLE IF NOT EXISTS categories (
                                id integer PRIMARY KEY,
                                name text NOT NULL
                              ); """
    my_db.create_table(sql_create_categories)

    sql_create_book_cats = """ CREATE TABLE IF NOT EXISTS book_categories (
                               book_category_id integer PRIMARY KEY,
                               book_id integer NOT NULL,
                               category_id integer NOT NULL,
                               FOREIGN KEY (book_id) REFERENCES books (id),
                               FOREIGN KEY (category_id) REFERENCES categories (id)
                             ); """

    my_db.create_table(sql_create_book_cats)

    sql_create_chapters = """ CREATE TABLE IF NOT EXISTS chapters (
                              id integer PRIMARY KEY,
                              wordcount integer,
                              content text,
                              originalchapterno integer,
                              relevant integer,
                              storychapterno integer,
                              book_id integer NOT NULL,
                              chapter_title text,
                              FOREIGN KEY (book_id) REFERENCES books (id)
                            );"""


if __name__ == '__main__':
    main()
