from flask_restful import Resource
from app.task import test


class TestNotification(Resource):
    def get(self, email):
        print("receiving email ..",email)
        test.delay(email, 'Coucou')
        return {'Message':'ok'}, 200