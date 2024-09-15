from flask_restful import Resource
from flask import request, session
from db.dbhandling import LIMIT, getTranscript, getTranscriptCount
from middleware.token_required import token_required


class VerifyPlan(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        if 'user_id' not in current_user:
            return {'error': 'Invalid token'}, 400
        limit_is_reach = getTranscriptCount(current_user['user_id']) >= LIMIT
        return limit_is_reach