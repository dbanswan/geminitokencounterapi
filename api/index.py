from flask import Flask, request
from flask_cors import CORS

# handle cors


import tiktoken

# from sanic import Sanic
# from sanic.response import json

# import nltk
cl100k_base = [
    "gpt-4",
    "gpt-3.5-turbo",
    "text-embedding-ada-002",
    "text-embedding-3-small",
    "text-embedding-3-large",
]
p50k_base = ["Codex models", "text-davinci-002", "text-davinci-003", "gpt-2"]
r50k_base = ["davinci", "curie", "babbage", "ada", "text-davinci-001"]
app = Flask(__name__)
# make sure we only access api from tokencounter.dbanswan.com
CORS(
    app,
    resources={
        r"/*": {
            "origins": "https://tokencounter.dbanswan.com",
            "methods": ["GET", "POST"],
        }
    },
)
# CORS(app)


@app.route("/tokenize", methods=["GET"])
def get_tokens():
    return "Welcome to the tokenization API!"


@app.route("/tokenize", methods=["POST"])
def count_tokens():

    encoding = tiktoken.get_encoding("cl100k_base")
    data = request.json
    text = data["text"]
    model = data["model"]
    encoding = ""
    if model in cl100k_base:
        encoding = tiktoken.get_encoding("cl100k_base")
    elif model in p50k_base:
        encoding = tiktoken.get_encoding("p50k_base")
    elif model in r50k_base:
        encoding = tiktoken.get_encoding("r50k_base")
    else:
        # send a 404 error with object {"error": true, "message": "Model not found in the list of models"} convert to json
        return {
            "error": True,
            "message": "Model not found in the list of models",
            data: None,
        }

    num_tokens = len(encoding.encode(text))

    return {"error": False, "message": "Token count successful", "data": num_tokens}


# if __name__ == "__main__":
#     # app.run(debug=True)
#     from waitress import serve

#     serve(app, host="127.0.0.1", port=5000)


# from flask import Flask


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/about")
def about():
    return "About"
