from crypt import methods
from email import header
from flask import Flask, abort, Response, request
import requests
from flask_cors import CORS
import jwt


app = Flask(__name__)
CORS(app)

USER_API_URL = "http://music-app-user-api.azurewebsites.net:80"
GROUP_API_URL = "http://groups-api-service:80"


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

    decoded_payload = jwt.decode(
        token,
        "django-insecure-a5l-_(w@to0la2u_y0vzc8+$gwp^p&e*)%hr6dh7$9-y#cvz=!",  # taken from django config SECRET_KEY
        algorithms=["HS256"],
    )
    return decoded_payload


@app.route("/api/token/refresh/", methods=["POST"])
def refresh():
    if request.method == "POST":
        data = request.get_json()
        resp = requests.post(
            USER_API_URL + "/backend/token/refresh/",
            headers={"accept": "application/json"},
            json=data,
        )
        return (resp.text, resp.status_code, resp.headers.items())


@app.route("/api/login/", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        resp = requests.post(
            USER_API_URL + "/backend/token/login/",
            headers={"accept": "application/json"},
            json=data,
        )
        return (resp.text, resp.status_code, resp.headers.items())


@app.route("/api/users/", methods=["GET", "POST"])
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


@app.route("/api/users/<user_id>", methods=["GET"])
def user(user_id):
    resp = requests.get(USER_API_URL + "/backend/users/" + user_id + "/")
    return (resp.text, resp.status_code, resp.headers.items())


@app.route("/api/groups/", methods=["GET", "POST"])
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


@app.route("/api/groups/<group_id>", methods=["GET", "PUT", "DELETE"])
def group(group_id):
    if request.method == "GET":
        resp = requests.get(GROUP_API_URL + "/groups/" + group_id)

    if request.method == "PUT":
        token = request.headers.get("Authorization")
        data = request.get_json()
        if authorize(token=token)["user_id"] == data["user_id"]:
            resp = requests.put(
                GROUP_API_URL + "/groups/" + group_id,
                headers={"accept": "application/json"},
                json=data,
            )

    if request.method == "DELETE":
        token = request.headers.get("Authorization")
        data = request.get_json()
        if authorize(token=token)["user_id"] == data["user_id"]:
            resp = requests.delete(GROUP_API_URL + "/groups/" + group_id)

    return (resp.text, resp.status_code, resp.headers.items())


@app.route("/api/groups/<group_id>/join", methods=["POST"])
def join_group(group_id):
    token = request.headers.get("Authorization")
    data = request.get_json()
    if authorize(token=token)["user_id"] == data["user_id"]:
        resp = requests.post(
            GROUP_API_URL + "/groups/" + group_id + "/join/",
            headers={"accept": "application/json"},
            json=data,
        )
        return (resp.text, resp.status_code, resp.headers.items())


@app.route("/api/groups/<group_id>/leave", methods=["POST"])
def leave_group(group_id):
    token = request.headers.get("Authorization")
    data = request.get_json()
    if authorize(token=token)["user_id"] == data["user_id"]:
        resp = requests.post(
            GROUP_API_URL + "/groups/" + group_id + "/leave/",
            headers={"accept": "application/json"},
            json=data,
        )
        return (resp.text, resp.status_code, resp.headers.items())


@app.route("/api/groups/users", methods=["GET"])
def group_users():
    resp = requests.get(GROUP_API_URL + "/users/")
    return (resp.text, resp.status_code, resp.headers.items())
