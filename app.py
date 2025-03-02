from flask import Flask, request, render_template_string
import requests
import json
import random
import re

app = Flask(name)

# API URL for player data
url_1 = 'https://topup.pk/api/auth/player_id_login'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': 'source=mb; region=PK; mspid2=d4c6befc082167a69a582be555056eee; datadome=7FV6UMLh4wB~rE7JKEttGo03crCDmfGi5vIT9AcY4C8~xjgRU1qaJzuF_nCDUkBUTMCEQiudMiLn2zOatSRdeCfnkqpBciARpYQP8CtVV6mbA_yK7HTTXxLVRuLuLbY~; _ga=GA1.1.1432169104.1733537832; session_key=flh7i9330kb0o9z5t6zr5dxnfd7aagg3; _ga_C956TFJLD0=GS1.1.1733537831.1.0.1733537842.0.0.0',
    'Origin': 'https://topup.pk',
    'Pragma': 'no-cache',
    'Referer': 'https://topup.pk/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"'
}

@app.route('/get_player_data', methods=['GET'])
def get_player_data():
    uid = request.args.get('uid')

    # Check if UID is provided
    if not uid:
        return "UID is required", 400

    # Check if UID is valid (numeric and within the range of 8-10 digits)
    if not uid.isdigit() or len(uid) < 8 or len(uid) > 10:
        return "Invalid UID. UID must be numeric and between 8-10 digits.", 400

    # Call the external API (topup.pk) with the UID
    data_1 = {'app_id': 100067, 'login_id': uid}
    response = requests.post(url_1, headers=headers, data=json.dumps(data_1))

    if response.status_code != 200:
        return f"Failed to fetch data from API. Status code: {response.status_code}", 500

    # Parse the response data
    data_1_json = response.json()

    # Check if expected fields are present in the response
    nickname = data_1_json.get('nickname', 'not found')
    region_from_api = data_1_json.get('region', 'not found')

    if nickname == 'not found' or region_from_api == 'not found':
        return "Failed to retrieve valid data from the API.", 500

    # Clean the nickname by removing non-ASCII characters
    cleaned_nickname = re.sub(r'[^\x00-\x7F]+', '', nickname)

    # Generate random "like after" number between 6000 and 12000
    like_after = random.randint(15000, 45000)

    # Prepare the response data in the desired format (one per line)
    response_text = f"APP LINK : https://t.me/Freefirelikess<br>"
    response_text += f"PLAYER NICKNAME : {cleaned_nickname}<br>"
    response_text += f"PLAYER REGION : {region_from_api}<br>"
    response_text += f"LIKE AFTER COMMAND : {like_after}<br>"
    response_text += f"LIFE BEFORE : +0<br>"
    response_text += f"PLAYER UID : {uid}<br>"

    # HTML Template with black background and white text
    html_template = """
    <html>
        <head>
            <style>
                body {
                    background-color: black;
                    color: white;
                    font-family: Arial, sans-serif;
                    font-size: 20px;
                    padding: 20px;
                }
                h1 {
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>GLFF LIKE</h1>
            {{ response_text|safe }}
        </body>
    </html>
    """

    return render_template_string(html_template, response_text=response_text)

if name == 'main':
    app.run(debug=True)
