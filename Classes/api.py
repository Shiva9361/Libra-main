from init import app
from flask_restful import Resource,reqparse
from Classes.Dbmodels import Book

app.app_context().push()

errors = {
    "NFB":"Book not found"
}
class bookResource(Resource):
    def get(self, book_id):
        book = Book.query.filter_by(book_id == book_id).first()
        if book is None:
            return errors['NFB'],404
        
        return {'ID': book.book_id,'Name': book.book_name,
                'Authors':book.authors},200