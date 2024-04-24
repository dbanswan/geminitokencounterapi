# Token Counter For Text Based Gemini Models

A very simple implementation of token counter for gemini models.

You can always use the token counter directly in the python code when making request to gemini api to give you live token count of your prompt and responses with a simple python line :

```python
num_tokens = gemini_model.count_tokens(text).total_tokens
```

This was made to give a api endpoint where requests can be made to get token count in prompts.

**Currently tracking following models. Support for vision, image models coming soon**

```python
gemini_models = [
    "gemini-1.0-pro",
    "gemini-1.0-pro-001",
    "gemini-1.0-pro-latest",
    "gemini-1.5-pro-latest",
    "gemini-pro",
]
```

## Prerequisite

- Get your API_KEY from [google ai studio](https://aistudio.google.com/app/apikey),

- rename .env_local to .env
- replace API_KEY with yours in .env

Counter is exposed through post request on /tokenize endpoint. We need to send json payload to the endpoint e.g http://127.0.0.1:5000/tokenize as:

<img src="https://raw.githubusercontent.com/dbanswan/geminitokencounterapi/main/request.png" alt="token counter api request"/>

```json
{ "text": "count tokens in this prompt", "model": "gemini-1.0-pro" }
```

```python
# And we are extracting details from request as following
data = request.json
text = data["text"]
model = data["model"]

```

If the model matches to the ones are tracking the json response will be following format :

```json
{
  "data": 27,
  "error": false,
  "message": "Token count successful"
}
```

Unsuccessful response:

```json
{
    "error": True,
    "message": "Error counting tokens",
    "data": -1
}
```

CORS comes into question as we deploy our api endpoint to production. This is tracked using the environment key in the .env file.

```python
# Make sure to change the origins to your web app url post requests are coming from
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

```

When set to "dev" CORS will be off, change it to "prod" on deployment (I use vercel so in the project settings can add env variables).
