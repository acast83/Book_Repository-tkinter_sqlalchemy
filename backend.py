from db_model import Db_Model, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


Session = sessionmaker(bind=engine)
session = Session()


class Backend:

    def insert(self, title_data, author_data, year_data, isbn_data):
        try:
            book = Db_Model(title=title_data, author=author_data,
                            year=year_data, isbn=isbn_data)
            session.add(book)
            session.commit()
        except Exception as e:
            print(f"Error, {e}")
        finally:
            session.close()

    def view(self,):
        books = session.query(Db_Model).all()
        session.close()
        return books

    def delete(self, id):
        book = session.query(Db_Model).filter(Db_Model.id == id).first()
        session.delete(book)
        session.commit()
        session.close()

    def search(self, title_data, author_data, year_data, isbn_data):
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

    def update(self, id, title, author, year, isbn):
        book = session.query(Db_Model).filter(Db_Model.id == id).first()
        book.title = title
        book.author = author
        book.year = year
        book.isbn = isbn
        session.commit()
        session.close()
