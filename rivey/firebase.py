import pyrebase

def firebase_init():
    config = {
    'apiKey': "AIzaSyCIv6kDfzIptn9R0h8ktGJ_I7ENNRJ7l0o",
    'authDomain': "rivey-sw.firebaseapp.com",
    'projectId': "rivey-sw",
    'storageBucket': "rivey-sw.appspot.com",
    'messagingSenderId': "234525462180",
    'appId': "1:234525462180:web:b36863987ab25a29e96031",
    'measurementId': "G-4ZFKTVMHRC",
    'databaseURL' : ''
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()

    return auth

auth = firebase_init()