from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

google_api_key = os.getenv("API_KEY")
# print(google_api_key)
genai.configure(api_key=google_api_key)
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
gemini_models = [
    "gemini-1.0-pro",
    "gemini-1.0-pro-001",
    "gemini-1.0-pro-latest",
    "gemini-1.0-pro-vision-latest",
    "gemini-1.5-pro-latest",
    "gemini-pro",
    "gemini-pro-vision",
]

app = Flask(__name__)
# make sure we only access api from tokencounter.dbanswan.com
CORS(
    app,
    resources={
        r"/*": {
            "origins": ["https://tokencounter.dbanswan.com", "http://localhost:3000"],
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
    try:

        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = 0
        data = request.json
        text = data["text"]
        model = data["model"]
        encoding = ""
        if model in gemini_models:
            # google_api_key = os.getenv("API_KEY")
            # print(google_api_key)
            # genai.configure(api_key=google_api_key)
            model = "models/" + model
            gemini_model = genai.GenerativeModel(model)
            num_tokens = gemini_model.count_tokens(text).total_tokens
            # print(type(num_tokens))

            # num_tokens = num_tokens.split("total_tokens: ")[1]
            print(num_tokens)

        elif model in cl100k_base:
            encoding = tiktoken.get_encoding("cl100k_base")
            num_tokens = len(encoding.encode(text))

        elif model in p50k_base:
            encoding = tiktoken.get_encoding("p50k_base")
            num_tokens = len(encoding.encode(text))
        elif model in r50k_base:
            encoding = tiktoken.get_encoding("r50k_base")
            num_tokens = len(encoding.encode(text))
        else:
            # send a 404 error with object {"error": true, "message": "Model not found in the list of models"} convert to json
            return {
                "error": True,
                "message": "Model not found in the list of models",
                "data": -1,
            }

        return {"error": False, "message": "Token count successful", "data": num_tokens}
    except:
        return {"error": True, "message": "Error counting tokens", "data": -1}


if __name__ == "__main__":
    # app.run(debug=True)
    from waitress import serve

    # for m in genai.list_models():
    #     if "generateContent" in m.supported_generation_methods:
    #         print(m.name)
    print("Server Started")
    serve(app, host="127.0.0.1", port=5000)


# from flask import Flask


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/about")
def about():
    return "About"
