from flask_restful import Resource
from flask import request, session
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBZsN6q3radjhi8RYsxLutVCNwBOpm6558",
  "authDomain": "kairot-bc1ec.firebaseapp.com",
  "projectId": "kairot-bc1ec",
  "storageBucket": "kairot-bc1ec.appspot.com",
  "messagingSenderId": "570794221326",
  "appId": "1:570794221326:web:5fa4affe0767840392415f",
  "databaseURL": ''
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
class Login(Resource):
    def get(self):
        return "Hello, World!"
    
    def post(self):
        data = request.get_json()
        if 'email' not in data or 'password' not in data:
            return {'error': 'Missing email or password'}, 400
        if data['email'] and data['password']:
            try:
                user = auth.sign_in_with_email_and_password(data['email'], data['password'])
                session['idToken'] = user['idToken']
            except Exception as e:
                return {'error': 'Invalid email or password', 'error': str(e)}, 400
        return user

class Logout(Resource):
    def get(self):
        try:
            session.pop('idToken', None)
            return {'message': 'Logged out'}
        except: return {'error': 'Not logged in'}, 400

class SignUp(Resource):
    def get(self):
        return "Hello, World!"
    
    def post(self):
        data = request.get_json()
        if 'email' not in data or 'password' not in data:
            return {'error': 'Missing email or password'}, 400
        if data['email'] and data['password']:
            try:
                user = auth.create_user_with_email_and_password(data['email'], data['password'])
            except Exception as e:
                print(e)
                return {'error': str(e)}, 500
            return user
        return data
    
class ResetPassword(Resource):
    def get(self):
        return "Hello, World!"
    
    def post(self):
        data = request.get_json()
        if 'email' not in data:
            return {'error': 'Missing email'}, 400
        if data['email']:
            try:
                auth.send_password_reset_email(data['email'])
                return {'message': 'Password reset email sent'}
            except Exception as e:
                return {'error': str(e)}, 500
        return {'error': 'Missing email'}, 400


class VerifyToken(Resource):
    def get(self):
        return 'Verify token'
    
    def post(self):
        data = request.get_json()
        
        if 'token' not in data:
            return {'error': 'Missing token'}, 400
        if data['token']:
            if 'token' in session:
                if session['token'] == data['token']:
                    return {'message': 'Token verified'}, 200
        return {'error': 'Invalid token'}, 400
            