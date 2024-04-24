import os
import google.generativeai as genai

from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()

google_api_key = os.getenv("API_KEY")
environment = os.getenv("ENVIRONMENT")

genai.configure(api_key=google_api_key)
gemini_models = [
    "gemini-1.0-pro",
    "gemini-1.0-pro-001",
    "gemini-1.0-pro-latest",
    "gemini-1.5-pro-latest",
    "gemini-pro",
]

app = Flask(__name__)
# make sure we only access api from tokencounter.dbanswan.com
if environment != "dev":
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "https://geminitokencounter.dbanswan.com",
                ],
                "methods": ["GET", "POST"],
            }
        },
    )

# do not add / in the end of any url here or for any other project. https://example.com/ will not work https://example.com will


@app.route("/tokenize", methods=["GET"])
def get_tokens():
    return "Welcome to the tokenization API!"


@app.route("/tokenize", methods=["POST"])
def count_tokens():
    try:
        num_tokens = 0
        data = request.json
        text = data["text"]
        model = data["model"]
        encoding = ""
        if model in gemini_models:
            model = "models/" + model
            gemini_model = genai.GenerativeModel(model)
            num_tokens = gemini_model.count_tokens(text).total_tokens
            if environment == "dev":
                print(num_tokens)

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
    if environment == "dev":
        app.run(debug=True)
    from waitress import serve

    print("Server Started")
    serve(app, host="127.0.0.1", port=5000)
