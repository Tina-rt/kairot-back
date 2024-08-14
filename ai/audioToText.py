import google.generativeai as genai
import dotenv, os, json

dotenv.load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash", generation_config={
    "response_mime_type": "application/json",
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    })

def audioToText(audio:bytes, mimetype, language=None):
    if language is None:
        prompt = "Transcribe this audio into this format {\n                \"timeline\": [\n                   {\"start\": 111.0, \"end\": 112.0, \"text\": \"Every two weeks\"},\n                   {\"start\": 1.0, \"end\": 1.5, \"text\": \"things are going well\"}, \n                   {\"start\": 1.5, \"end\": 1.8, \"text\": \"and business is start\"}, \n                   {\"start\": 1.8, \"end\": 2.4, \"text\": \"ing to pick up\"}\n                ]\n            }\n"
    else:
        prompt = f"Transcribe the following audio in json format in {language} with range timeline: "
    response = model.generate_content([prompt, {
        "mime_type": mimetype,
        "data": audio
    }]) 
    
    print(response.text)
    
    return json.loads(response.text)
        