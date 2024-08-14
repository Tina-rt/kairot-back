import json
from flask_restful import Resource, reqparse
import werkzeug
from werkzeug.utils import secure_filename
import os, time
from ai.audioToText import audioToText

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
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        if 'file' not in args:
            return {'error': 'No file part'}, 400
        file = args['file']
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
            time.sleep(4)
            print("Fetching text from audio...")
            try:
                # result = audioToText(file.read())
                # result = json.loads(result)
                result = self.process_response(result)
            except:
                return {'error': 'Something went wrong (Audio may unsafe)'}, 500
            return result
        return {'error': 'No file part'}, 400
            # return {'message': 'File transferred successfully', 'filename': filename}, 200