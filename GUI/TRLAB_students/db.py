
import firebase_admin
from  firebase_admin import credentials
from firebase_admin import db

key = 'account.json'

class DataBase():

    def __init__(self, *args, **kwargs):
        self.key = key
        self.cred = credentials.Certificate(self.key)
        self.connected = False
        self.connect()
        self.ref = db.reference('')

    def connect(self):
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': 'https://tavo-robotas.firebaseio.com/'
        })


    def print_db(self):
        print(self.ref .get())