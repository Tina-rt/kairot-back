from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from app.api.audioToText import AudioToText
from app.api.auth import Login, Logout, SignUp, ResetPassword, VerifyToken
from app.api.documents import DocumentsList, Document
from app.api.verify_plan import VerifyPlan
from app.api.test import TestNotification

from flask_socketio import SocketIO, emit

socketio = SocketIO(message_queue="redis://redis:6379/0", cors_allowed_origins="*")



def create_app():
    app = Flask(__name__)
    app.secret_key = 'KAKAROT'
    api = Api(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    api.add_resource(AudioToText, '/audioToText')
    api.add_resource(Login, '/login')
    api.add_resource(SignUp, '/signup')
    api.add_resource(ResetPassword, '/resetPassword')
    api.add_resource(VerifyToken, '/verifyToken')
    api.add_resource(Logout, '/logout')
    api.add_resource(DocumentsList, '/documents')
    api.add_resource(Document, '/documents/<doc_id>')
    api.add_resource(VerifyPlan, '/limitIsReach')
    api.add_resource(TestNotification, '/test/<email>')

    socketio.init_app(app)
    return app


