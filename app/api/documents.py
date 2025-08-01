from flask_restful import Resource
from flask import request, session
from app.db.dbhandling import getTranscript, deleteTranscript
from app.middleware.token_required import token_required


class DocumentsList(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        if 'user_id' not in current_user:
            return {'error': 'Invalid token'}, 400
        data = getTranscript(current_user['user_id'])
        return data

class Document(Resource):
    method_decorators = [token_required]

    def delete(self, current_user, doc_id):
        if 'user_id' not in current_user:
            return {'error': 'Invalid token'}, 400
        data = deleteTranscript(current_user['user_id'], doc_id)
        return data
