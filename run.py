# from flask import Flask
# from flask_cors import CORS
# from flask_restful import Api

# from api.audioToText import AudioToText
# from api.auth import Login, Logout, SignUp, ResetPassword, VerifyToken
# from api.documents import Documents
# from api.verify_plan import VerifyPlan

# from flask_socketio import SocketIO, emit



# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins='*')

# app.secret_key = 'KAKAROT'

# api = Api(app)
# CORS(app, resources={r"/*": {"origins": "*"}})

# api.add_resource(AudioToText, '/audioToText')
# api.add_resource(Login, '/login')
# api.add_resource(SignUp, '/signup')
# api.add_resource(ResetPassword, '/resetPassword')
# api.add_resource(VerifyToken, '/verifyToken')
# api.add_resource(Logout, '/logout')
# api.add_resource(Documents, '/documents')
# api.add_resource(VerifyPlan, '/limitIsReach')

# if __name__ == '__main__':
#     app.run(debug=True)

from app import create_app, socketio
app = create_app()
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)