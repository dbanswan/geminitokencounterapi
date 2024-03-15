from flask import Flask, request
import tiktoken

# import nltk
cl100k_base = [
    "gpt-4",
    "gpt-3.5-turbo",
    "text-embedding-ada-002",
    "text-embedding-3-small",
    "text-embedding-3-large",
]
p50k_base = ["Codex models", "text-davinci-002", "text-davinci-003"]
r50k_base = ["davinci", "curie", "babbage", "ada", "text-davinci-001"]

app = Flask(__name__)

##nltk.download('punkt')
# from nltk.tokenize import word_tokenize


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
        return f"Model {model} not found in the list of models"

    num_tokens = len(encoding.encode(text))

    return f"The number of tokens in the text is: {num_tokens}"


if __name__ == "__main__":
    # app.run(debug=True)
    from waitress import serve

    serve(app, host="127.0.0.1", port=5000)
