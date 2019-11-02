import os, requests, uuid, json

# Don't forget to replace with your Cog Services subscription key!
# If you prefer to use environment variables, see Extra Credit for more info.
filename = "api_key.txt"
api_file = open(filename, "r")
api_key = api_file.readlines()

# Don't forget to replace with your Cog Services location!
# Our Flask route will supply two arguments: text_input and language_output.
# When the translate text button is pressed in our Flask app, the Ajax request
# will grab these values from our web app, and use them in the request.
# See main.js for Ajax calls.
def get_translation(text_input, language_output):
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=' + language_output
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': api_key[0].rstrip(),
        'Ocp-Apim-Subscription-Region': api_key[1].rstrip(),
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text' : text_input
    }]
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()

print(get_translation("再试一次，包括他的ETF援助给我的东西，不是胡言乱语。", "en-US"))
print(get_translation("incluyendo su ayuda ETF dame algo que no sea", "en-US"))