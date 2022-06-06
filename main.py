import ebooklib
from db_setup import SQLiteDatabase
from ebooklib import epub
import book_processor


class BookAnalyser:
    def __init__(self, bookpath):
        try:
            self.active_book = epub.read_epub(bookpath)
            self.active_db = SQLiteDatabase('default.db')
            print(f"Successfully opened {bookpath}. Use add_book to add to database")
        except FileNotFoundError as e:
            print(f"File {bookpath} not found.")
            raise

    def add_book(self):
        book_title = book_processor.get_title(self.active_book)
        book_author = book_processor.get_author(self.active_book)
        author_id = self.active_db.insert_author(book_author)

