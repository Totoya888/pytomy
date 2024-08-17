import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FirebaseController:
  def __init__(self):
    cred = credentials.Certificate("firebase_controller/automy_firebase_admin.json")
    firebase_admin.initialize_app(cred)
    self.db = firestore.client()

  def get_db(self):
    return self.db