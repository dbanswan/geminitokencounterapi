import os
import google.generativeai as genai
from flask_caching import Cache
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()

google_api_key = os.getenv("API_KEY")
environment = os.getenv("ENVIRONMENT")


genai.configure(api_key=google_api_key)
gemini_models = []

# right now there are 2 types of count tokens methods one for embedding models and rest for others, we are going to ignore non-text models for now
token_count_methods = ["countTextTokens", "countTokens"]

app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})
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
else:
    CORS(app)

# do not add / in the end of any url here or for any other project. https://example.com/ will not work https://example.com will


@app.route("/tokenize", methods=["GET"])
def get_tokens():
    return "Welcome to the tokenization API!"


@app.route("/listmodels", methods=["GET"])
@cache.cached(timeout=72000)
def listmodels():
    try:
        models = genai.list_models()
        allmodels = []
        for model in models:
            allmodels.append(model)
        gemini_models = []

        for models in allmodels:
            model_name = models.name
            model_supported_generation_methods = models.supported_generation_methods
            input_tokens_limit = models.input_token_limit
            output_tokens_limit = models.output_token_limit

            for method_type in token_count_methods:
                if method_type in model_supported_generation_methods:
                    model_token_count_method = method_type

            gemini_models.append(
                {
                    "model_name": model_name,
                    "token_count_method": model_token_count_method,
                    "input_token_limit": input_tokens_limit,
                    "output_token_limit": output_tokens_limit,
                }
            )

        return {"models": gemini_models}
    except Exception as e:
        print(e)
        return {"error": e}


@app.route("/tokenize", methods=["POST"])
def count_tokens():
    try:
        num_tokens = 0
        data = request.json
        text = data["text"]
        model = data["model"]

        gemini_models = listmodels()["models"]
        # print(gemini_models)
        for models in gemini_models:
            if models["model_name"] == model:
                print(f" token count method {models["token_count_method"]}")
                if models["token_count_method"] == "countTokens":
                    gemini_model = genai.GenerativeModel(model)
                    num_tokens = gemini_model.count_tokens(text).total_tokens
                    if environment == "dev":
                        print(num_tokens)
                else:
                    return {"error": True, "message": "Model Not Supported", "data": -1}

        # if model in gemini_models:
        #     model = "models/" + model
        #     gemini_model = genai.GenerativeModel(model)
        #     num_tokens = gemini_model.count_tokens(text).total_tokens
        #     if environment == "dev":
        #         print(num_tokens)

        # else:
        #     # send a 404 error with object {"error": true, "message": "Model not found in the list of models"} convert to json
        #     return {
        #         "error": True,
        #         "message": "Model not found in the list of models",
        #         "data": -1,
        #     }

        return {"error": False, "message": "Token count successful", "data": num_tokens}
    except Exception as e:
        print(e)
        return {"error": True, "message": "Error counting tokens", "data": -1}


if __name__ == "__main__":
    if environment == "dev":
        app.run(debug=True)
    from waitress import serve

    print("Server Started")
    listmodels()
    serve(app, host="127.0.0.1", port=5000)
