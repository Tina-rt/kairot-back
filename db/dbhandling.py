if __name__ == '__main__':
    from firebase_db import db, storage
else:
    from db.firebase_db import db, storage

import json, datetime
from io import BytesIO


def newTranscript(transcripted, user_id, audio_file: bytes, audio_name: str):
    try:
        try:
            bucket = storage.bucket()
            blob = bucket.blob(audio_name)
            blob.upload_from_file(BytesIO(audio_file))
        except Exception as e: return {'error': 'Failed to upload transcript', 'error_message': str(e)}, 500
        
        
        data = {
            'transcripted': transcripted,
            'created_at': datetime.datetime.now().isoformat(),
            'audio_file': blob.public_url,
            'audio_filename': audio_name
        }
        doc_ref = db.collection(user_id).document()
        doc_ref.set(data)
        print(doc_ref.id)
        # user_ref = db.
    except Exception as e: 
        return {'error': 'Failed to upload transcript', 'error_message': str(e)}, 500
    return {'message': 'Transcript uploaded'}, 200

def getTranscript(user_id):
    try:
        docs = db.collection(user_id).order_by("created_at").get()
        result = []
        for doc in docs:
            # print(doc.to_dict())
            result.append(doc.to_dict())
        return result[::-1]
    except Exception as e: return {'error': 'Failed to get transcript', 'error_message': str(e)}, 500
# print(newTranscript({
#   "timeline": [
#     {
#       "start": 111.0,
#       "end": 112.0,
#       "text": "Every two weeks"
#     },
#     {
#       "start": 1.0,
#       "end": 1.5,
#       "text": "things are going well"
#     },
#     {
#       "start": 1.5,
#       "end": 1.8,
#       "text": "and business is start"
#     },
#     {
#       "start": 1.8,
#       "end": 2.4,
#       "text": "ing to pick up"
#     }
#   ],
#   "timeline_text": "Every two weeks things are going well and business is start ing to pick up ",
#   "timeline_time_text": "111.0-112.0 : Every two weeks\n1.0-1.5 : things are going well\n1.5-1.8 : and business is start\n1.8-2.4 : ing to pick up\n"
# }, 'p8EkDSj9Z3bsb4qXBvXSp1aLp4p1'))

# print(getTranscript('p8EkDSj9Z3bsb4qXBvXSp1aLp4p1'))