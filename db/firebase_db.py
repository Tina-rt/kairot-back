import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("key/kairot-bc1ec-firebase-adminsdk-gwr0g-03f1ec2af1.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'kairot-bc1ec.appspot.com'
})

db = firestore.client()

firebaseConfig = {
  "apiKey": "AIzaSyBZsN6q3radjhi8RYsxLutVCNwBOpm6558",
  "authDomain": "kairot-bc1ec.firebaseapp.com",
  "projectId": "kairot-bc1ec",
  "storageBucket": "kairot-bc1ec.appspot.com",
  "messagingSenderId": "570794221326",
  "appId": "1:570794221326:web:5fa4affe0767840392415f",
  "databaseURL": 'https://kairot-bc1ec.firebaseio.com/'
}

firebase = pyrebase.initialize_app(firebaseConfig)
