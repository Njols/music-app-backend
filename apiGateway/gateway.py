from email import header
from flask import Flask, abort, Response, request
import requests
from flask_cors import CORS
import jwt


app = Flask(__name__)
CORS(app)

USER_API_URL = "http://backend:8000"


@app.route("/token/refresh/", methods=["POST"])
def refresh():
    if request.method == "POST":
        data = request.get_json()
        resp = requests.post(
            USER_API_URL + "/backend/token/refresh/",
            headers={"accept": "application/json"},
            json=data,
        )
        return (resp.text, resp.status_code, resp.headers.items())


@app.route("/login/", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        resp = requests.post(
            USER_API_URL + "/backend/token/login/",
            headers={"accept": "application/json"},
            json=data,
        )
        return (resp.text, resp.status_code, resp.headers.items())


@app.route("/users/", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        resp = requests.get(USER_API_URL + "/backend/users/")

        return (resp.text, resp.status_code, resp.headers.items())
    if request.method == "POST":
        data = request.get_json()
        resp = requests.post(
            USER_API_URL + "/backend/users/",
            headers={"accept": "application/json"},
            json=data,
        )

        return (resp.text, resp.status_code, resp.headers.items())
