import google.generativeai as genai
import dotenv, os, json

dotenv.load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"response_mime_type": "application/json"})

def audioToText(audio:bytes, mimetype, language=None):
    if language is None:
        prompt = f"Transcribe the following audio in json format: "
    else:
        prompt = f"Transcribe the following audio in json format in {language}: "
    response = model.generate_content(prompt, {
        "mime_type": mimetype,
        "data": audio
    }) 
    
    return json.loads(response.text)
        