from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import os
import requests, json

wpp_url = os.environ["WHATSAPP_API_URL"]
chat_id = os.environ["CHAT_ID"]

def send_notification(alert):
    if alert['status'] == "firing":
        status_emoji = "🚨"
    else:
        status_emoji = "✅"
    content = f"📌 {alert['name']}\n{status_emoji} {alert['status']}\n🌐 {alert['dashboard']}"
    payload = json.dumps({
        "chatId": chat_id,
        "contentType": "string",
        "content": content
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", wpp_url, headers=headers, data=payload, verify=False)
    if response.status_code == 200:
        print("> whatsapp message sent")
    else:
        print(f"Error {response.status_code} sending message\n")
        print(response.text)

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

@app.route('/', methods=['POST'])
def webhook():
    alert = {}
    data = request.json
    alert["name"] = data['alerts'][0]['labels']['alertname']
    alert["status"] = data['alerts'][0]['status']
    alert["dashboard"] = data['alerts'][0]['dashboardURL']
    print(f"> received alert")
    print(alert)
    try:
        send_notification(alert)
        return "notification sent"
    except Exception as e:
        print(f"> error, {e}")
    

app.run(host="0.0.0.0", port=5000)