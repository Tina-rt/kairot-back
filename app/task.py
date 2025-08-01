from celery import Celery
from app.ai.audioToText import Transcripted, audioToText
from app.db.dbhandling import newTranscript, updateTranscription
from flask_socketio import SocketIO

socketio = SocketIO(message_queue="redis://redis:6379/0")


celery = Celery('worker', broker="redis://redis:6379/0")


def process_response( response: list[Transcripted]):
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

@celery.task
def transcribe_audio(file_byte, filename, user_id):
    result = None
    try:
        upload_output, status = newTranscript({}, user_id, file_byte, filename)
        doc_ref = upload_output['doc_ref']
        result = audioToText(file_byte)
    except Exception as e: 
        print(e)
        socketio.emit(f"user-{user_id}", {
            "status": 500,
            "title": "Transcription failed",
            "info": {'message': "Creating transcription or ai failed", 'detail': str(e)},
            "filename": filename,
        })
    if result is None:
        socketio.emit(f"user-{user_id}", {
            "status": 500,
            "title": "Transcription failed",
            "info": {'message': "Creating transcription or ai failed", 'detail': str(e)},
            "filename": filename,
        })
        return
    result = process_response(result)
    updateTranscription(user_id, doc_ref.id, 'transcripted', result)
    upload_output, status = updateTranscription(user_id, doc_ref.id, 'status', 1)
    print(upload_output)
    if status == 200:

        socketio.emit(f"user-{user_id}", {
            "status": status,
            "title": "Transcription finished",
            "info": upload_output,
            "filename": filename,
        })
    else:
        socketio.emit(f"user-{user_id}", {
            "status": status,
            "title": "Transcription failed",
            "info": upload_output,
            "filename": filename,
        })

    return "/documents/"

@celery.task
def test(myid, value):
    import time
    time.sleep(4)
    print("sending message")
    socketio.emit(f"{myid}", {
        "title": "OKKKK",
        "Url": value
    })
    return value