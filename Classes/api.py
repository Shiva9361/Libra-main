from init import app
from flask_restful import Api,Resource,reqparse


app.app_context().push()

class bookResource(Resource):
    def get(self, book_id):
        return 