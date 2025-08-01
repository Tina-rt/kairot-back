from google import genai
from google.genai import types
import dotenv, os, json
from pydantic import BaseModel

class Transcripted(BaseModel):
    text: str
    start: str
    end: str

dotenv.load_dotenv()

# genai.configure(api_key=os.environ.get("GEMINI_KEY"))


generation_config = {
    "response_mime_type": "application/json",
    "response_schema": list[Transcripted],
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    }
client = genai.Client()


def audioToText(audio:bytes, language=None) -> list[Transcripted]:
    if language is None:
        prompt = """Transcribe the following audio in the json format. 
            The end and start attributes is like HH:MM:SS.
            Transcribe each 4 second. 
            Return a list"""
    else:
        prompt = f"""Transcribe the following audio in json format in {language}  HH:MM:SS.
        The end and start attributes is like HH:MM:SS.
        Transcribe each 4 seconds minimum and 6 seconds max. s
        Return a list"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, 
            types.Part.from_bytes(
            data=audio,
            mime_type='audio/mp3',
            )
        ],
        config=generation_config
    ) 
    
    transcripted : list[Transcripted] = response.parsed
    print(transcripted)
    
    return transcripted
        