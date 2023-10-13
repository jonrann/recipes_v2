from flask import Flask

app = Flask(__name__)
app.secret_key = "a_secret_fora_secret"