import json
from flask_restful import Resource, reqparse
from flask import request
import werkzeug
from werkzeug.utils import secure_filename
import os, time
from app.ai.audioToText import Transcripted, audioToText
from app.db.dbhandling import LIMIT, getTranscriptCount, newTranscript
from app.task import transcribe_audio
import jwt

UPLOAD_FOLDER = 'uploads'

class AudioToText(Resource):
    def get(self):
        return "Hello, World!"
    
    def process_response(self, response: list[Transcripted]):
        concat_timeline = ''
        concat_timeline_text = ''
        result = {}
        print("parsing this list", response)
        for item in response:
            concat_timeline += item.text + ' '
            concat_timeline_text += f'{item.start}-{item.end} : {item.text}\n'
        result['timeline_text'] = concat_timeline
        result['timeline_time_text'] = concat_timeline_text
        result['timeline'] = [t.model_dump() for t in response]
        return result
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
            result = {}
            print("File content type", file.content_type)
            # time.sleep(2)
            print("Fetching text from audio...")
            try:
                file.seek(0)
                file_byte = file.read()
                print("Getting transcription count")
                total_transcript = getTranscriptCount(user_id)
                if total_transcript > LIMIT:
                    return {'error': 'Limit exceed', 'error_message': 'You reach the upload limit'}, 400
                print("Sending to celery task ...")
                transcribe_audio.delay(file_byte, filename, user_id)
                print("The Transcription is begining")
                return {'message': 'Transcription is begining'}, 200
            except Exception as e:
                print(e)
                return {'error': 'Something went wrong (Audio may unsafe)', 'error_message': str(e)}, 500
            return result
        return {'error': 'No file part'}, 400
            # return {'message': 'File transferred successfully', 'filename': filename}, 200