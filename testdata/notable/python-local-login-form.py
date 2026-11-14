from flask import Flask, request

app = Flask(__name__)

PAGE = '''<form method="post" action="/login">
<input name="email" type="email">
<input name="password" type="password">
<button>Continue</button></form>'''

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    return authenticate_user(email, password)
