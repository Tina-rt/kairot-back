from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.audioToText import AudioToText
from api.auth import Login, Logout, SignUp, ResetPassword, VerifyToken


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
if __name__ == '__main__':
    app.run(debug=True)

