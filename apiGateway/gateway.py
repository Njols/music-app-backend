from crypt import methods
from email import header
from flask import Flask, abort, Response, request
import requests
from flask_cors import CORS
import jwt


app = Flask(__name__)
CORS(app)

USER_API_URL = "http://backend:8000"
GROUP_API_URL = "http://groups:8000"


def authorize(token):
    if token is None:
        abort(Response("No token found", 400))
    token = token.split(" ")[1]

    authorize = requests.post(
        USER_API_URL + "/v1/token/verify/",
        headers={"accept": "application/json"},
        json={"token": token},
    )
    if authorize.status_code == 401:
        abort(401)


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


@app.route("/groups/", methods=["GET", "POST"])
def groups():
    if request.method == "GET":
        resp = requests.get(GROUP_API_URL + "/groups/")

        return (resp.text, resp.status_code, resp.headers.items())

    if request.method == "POST":
        data = request.get_json()
        resp = requests.post(
            GROUP_API_URL + "/groups/",
            headers={"accept": "application/json"},
            json=data,
        )

        return (resp.text, resp.status_code, resp.headers.items())


@app.route("/groups/<group_id>", methods=["GET", "PUT"])
def group(group_id):
    if request.method == "GET":
        resp = requests.get(GROUP_API_URL + "/groups/" + group_id)

    if request.method == "PUT":
        data = request.get_json()
        resp = requests.post(
            GROUP_API_URL + "/groups/" + group_id,
            headers={"accept": "application/json"},
            json=data,
        )

    return (resp.text, resp.status_code, resp.headers.items())


@app.route("/groups/users", methods=["GET"])
def group_users():
    resp = requests.get(GROUP_API_URL + "/users/")
    return (resp.text, resp.status_code, resp.headers.items())
