from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "your_verify_token")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.route("/chat/webhook", methods=["GET"])
def verify_webhook():
    """Verify webhook for WhatsApp"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/chat/webhook", methods=["POST"])
def handle_message():
    """Handle incoming WhatsApp messages"""
    try:
        data = request.get_json()
        print("=" * 50)
        print(f"Received webhook data: {data}")
        
        # Extract message details
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        print(f"Messages found: {len(messages)}")
        
        if not messages:
            print("No messages in webhook data")
            return jsonify({"status": "ok"}), 200
        
        message = messages[0]
        from_number = message.get("from")
        message_type = message.get("type")
        
        print(f"From: {from_number}, Type: {message_type}")
        
        # Only handle text messages
        if message_type == "text":
            text = message.get("text", {}).get("body", "")
            print(f"Text message: '{text}'")
            print(f"Attempting to send to {from_number}...")
            send_message(from_number, text)
        else:
            print(f"Ignoring non-text message type: {message_type}")
        
        print("=" * 50)
        return jsonify({"status": "ok"}), 200
    
    except Exception as e:
        print(f"ERROR in handle_message: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error"}), 200

def send_message(to_number, text):
    """Send echo message back via WhatsApp API"""
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }
    
    print(f"Sending to URL: {url}")
    print(f"Payload: {payload}")
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    return response

if __name__ == "__main__":
    app.run(port=5000, debug=True)
