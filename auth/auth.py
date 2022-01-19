import os
import time
from functools import wraps
import bcrypt
from werkzeug.exceptions import abort
import jwt
from jwt import ExpiredSignatureError
from flask import request, abort
from dotenv import load_dotenv

load_dotenv()

username1 = os.getenv('ADMIN_USER').encode()
password1 = os.getenv('ADMIN_PASSWORD').encode()

sir = os.getenv('SIR')
tuz = bcrypt.gensalt(12)
us = bcrypt.hashpw(username1, tuz)
pw = bcrypt.hashpw(password1, tuz)


def get_loged(username, password):
    username = username.encode()
    password = password.encode()
    if bcrypt.checkpw(username, us) and bcrypt.checkpw(password, pw):
        payload = {'role': 'admin', 'exp': (time.time() + 1800)}
        token = jwt.encode(payload, sir)
    else:
        abort(401, 'Qayta urunib ko`ring.')
    return token

def token_validator(token):
    if not token:
        abort(401, 'Admin sifatida kiring.')
    if len(token) == 0:
        abort(401, 'Token topilmadi.')
    return True

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token', None, str)
        if token_validator(token):
            try:
                payload = jwt.decode(token, sir, ['HS256'])
            except ExpiredSignatureError:
                abort(401, 'Iltimos. Qaytadan kiring.')
            except:
                abort(401, 'Admin sifatida kirish zarur.')
        return f(payload, *args, **kwargs)
    return decorated