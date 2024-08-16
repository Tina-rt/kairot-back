from flask_restful import Resource
from flask import request, session
from db.dbhandling import getTranscript
from middleware.token_required import token_required


class Documents(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        if 'user_id' not in current_user:
            return {'error': 'Invalid token'}, 400
        data = getTranscript(current_user['user_id'])
        return data