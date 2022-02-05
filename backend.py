from db_model import Db_Model, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import logging

# setting up a logger
logger = logging.getLogger(
    __name__
)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("book_repository.log")
logger.addHandler(file_handler)

formatter = logging.Formatter(
    "%(asctime)s:%(created)f:%(levelname)s:%(message)s"
)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

Session = sessionmaker(bind=engine)
session = Session()
session.expire_on_commit = False


class Backend:

    def insert(self, title_data, author_data, year_data, isbn_data):
        try:
            book = Db_Model(title=title_data, author=author_data,
                            year=year_data, isbn=isbn_data)
            session.add(book)
            session.commit()
            logger.info(
                f"Successfully added new book to the repository, id {book.id}")
        except Exception as e:
            logger.debug(f"Error, {e}")
        finally:
            session.close()

    def view(self,):
        try:
            books = session.query(Db_Model).all()
            session.close()
            return books
        except Exception as e:
            logger.debug(f"Error, {e}")

    def delete(self, id):
        try:
            book = session.query(Db_Model).filter(Db_Model.id == id).first()
            session.delete(book)
            session.commit()
            session.close()
            logger.info(
                f"Successfully removed book from the repository, id {id}")
        except Exception as e:
            logger.debug(f"Error, {e}")

    def search(self, title_data, author_data, year_data, isbn_data):
        try:
            if title_data != None:
                if " " or "-" in title_data:
                    keywords = title_data.split()
                    book_list = session.query(Db_Model).all()
                    results = []
                    for keyword in keywords:
                        for book in book_list:
                            if keyword.lower() in (book.title).lower():
                                results.append(book)
                    if len(results) != 0:
                        results = list(set(results))
                        return results

                else:
                    book_list = session.query(Db_Model).all()
                    results = []
                    for book in book_list:
                        if title_data in book.title:
                            results.append(book)
                    if len(results) > 0:
                        return results

            if author_data != None:
                books = session.query(Db_Model).filter(
                    func.lower(Db_Model.author) == func.lower(author_data)).all()
                session.close()
                if len(books) > 0:
                    return books

            if year_data != None:
                books = session.query(Db_Model).filter(
                    Db_Model.year == year_data).all()
                session.close()
                if len(books) > 0:
                    return books

            if isbn_data != None:
                books = session.query(
                    Db_Model).filter(Db_Model.isbn == isbn_data).all()
                session.close()
                if len(books) > 0:
                    return books
                else:
                    return
        except Exception as e:
            logger.debug(f"Error, {e}")

    def update(self, id, title, author, year, isbn):
        try:
            if title != None:
                book = session.query(Db_Model).filter(
                    Db_Model.id == id).first()
                book.title = title
                session.commit()
                session.close()
            if author != None:
                book = session.query(Db_Model).filter(
                    Db_Model.id == id).first()
                book.author = author
                session.commit()
                session.close()
            if year != None:
                book = session.query(Db_Model).filter(
                    Db_Model.id == id).first()
                book.year = year
                session.commit()
                session.close()
            if isbn != None:
                book = session.query(Db_Model).filter(
                    Db_Model.id == id).first()
                book.isbn = isbn
                session.commit()
                session.close()
            session.expunge_all()
            session.close()
            logger.info(f"Successfully mofified book entry, id {book.id}")
        except Exception as e:
            logger.debug(f"Error, {e}")
