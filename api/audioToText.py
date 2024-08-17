import json
from flask_restful import Resource, reqparse
from flask import request
import werkzeug
from werkzeug.utils import secure_filename
import os, time
from ai.audioToText import audioToText
from db.dbhandling import newTranscript
import jwt

UPLOAD_FOLDER = 'uploads'

class AudioToText(Resource):
    def get(self):
        return "Hello, World!"
    
    def process_response(self, response):
        concat_timeline = ''
        concat_timeline_text = ''
        if 'timeline' in response:
            for item in response['timeline']:
                concat_timeline += item['text'] + ' '
                concat_timeline_text += f'{item["start"]}-{item["end"]} : {item["text"]}\n'
            response['timeline_text'] = concat_timeline
            response['timeline_time_text'] = concat_timeline_text
        return response
    def post(self):
        print("Parsing file...")
        if 'Authorization' not in request.headers:
            print("No token")
            return {'error': 'No token'}, 400
        if request.headers['Authorization'] == '':
            print("Empty token")
            return {'error': 'Empty token'}, 400
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        if 'file' not in args:
            print("No file")
            return {'error': 'No file part'}, 400
        file = args['file']
        print("Token: ", request.headers['Authorization'])
        jwt_decoded = jwt.decode(request.headers['Authorization'], options={"verify_signature": False})
        if 'user_id' not in jwt_decoded:
            return {'error': 'Invalid token'}, 400
        user_id = jwt_decoded['user_id']
        if file:
            filename = secure_filename(file.filename)
            # result = ''
            result = {
                "timeline": [
                   {"start": 111.0, "end": 112.0, "text": "Every two weeks"},
                   {"start": 1.0, "end": 1.5, "text": "things are going well"}, 
                   {"start": 1.5, "end": 1.8, "text": "and business is start"}, 
                   {"start": 1.8, "end": 2.4, "text": "ing to pick up"}
                ]
            }
            print("File content type", file.content_type)
            # time.sleep(2)
            print("Fetching text from audio...")
            try:
                file_byte = file.read()
                result = audioToText(file_byte, file.content_type)
                result = self.process_response(result)
                upload_output = newTranscript(result, user_id, file_byte, filename)
                # print(upload_output)
                if 'error' in upload_output:
                    return {'error': upload_output['error'], 'error_message': upload_output['error_message']}, 500
            except Exception as e:
                return {'error': 'Something went wrong (Audio may unsafe)', 'error_message': str(e)}, 500
            return result
        return {'error': 'No file part'}, 400
            # return {'message': 'File transferred successfully', 'filename': filename}, 200