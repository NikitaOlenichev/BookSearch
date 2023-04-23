from flask_restful import abort, Resource
from flask import jsonify
from data.books import Book
from data import db_session


def abort_if_book_not_found(book_title):
    session = db_session.create_session()
    book = session.query(Book).filter(Book.title == book_title).first()
    if not book:
        abort(404, message=f"Books {book_title} not found")


class BookResource(Resource):
    def get(self, book_title):
        abort_if_book_not_found(book_title)
        session = db_session.create_session()
        book = session.query(Book).filter(Book.title == book_title).first()
        return jsonify({'book': book.to_dict()})

    def delete(self, book_id):
        abort_if_book_not_found(book_id)
        session = db_session.create_session()
        book = session.query(Book).get(book_id)
        session.delete(book)
        session.commit()
        return jsonify({'success': 'OK'})