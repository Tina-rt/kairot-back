import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore, storage
import dotenv, os

dotenv.load_dotenv()

cred_json = {
  "type": "service_account",
  "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
  "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
  "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace(r'\n', '\n'),
  "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
  "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL"),
  "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ.get("FIREBASE_STORAGE_BUCKET")
})

db = firestore.client()

firebaseConfig = {
  "apiKey": os.environ.get("FIREBASE_KEY"),
  "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN"),
  "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
  "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET"),
  "messagingSenderId": os.environ.get("MESSAGING_SENDER_ID"),
  "appId": os.environ.get("FIREBASE_APP_ID"),
  "databaseURL": os.environ.get("FIREBASE_DATABASE_URL")
}

firebase = pyrebase.initialize_app(firebaseConfig)
