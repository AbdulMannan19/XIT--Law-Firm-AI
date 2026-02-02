from flask import Flask, request, jsonify
import requests
from dependencies import VERIFY_TOKEN, ACCESS_TOKEN, PHONE_NUMBER_ID, API_VERSION

app = Flask(__name__)

@app.route("/chat", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/chat", methods=["POST"])
def handle_message():
    try:
        data = request.get_json()
        print(f"Webhook received: {data}")
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        if not messages:
            return jsonify({"status": "ok"}), 200
        
        message = messages[0]
        from_number = message.get("from")
        message_type = message.get("type")
        
        if message_type == "text":
            text = message.get("text", {}).get("body", "")
            send_message(from_number, text)
        
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error"}), 200

def send_message(to_number, text):
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }
    return requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
