import requests
from dependencies import ACCESS_TOKEN, PHONE_NUMBER_ID, API_VERSION

def send_whatsapp_message(to_number: str, body_text: str, preview_url: bool = False):
    """Send a text message via WhatsApp API"""
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {
            "preview_url": preview_url,
            "body": body_text
        }
    }
    
    print(f"Sending to: {to_number}")
    print(f"Message: {body_text}")
    print(f"URL: {url}")
    
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    return response

if __name__ == "__main__":
    test_number = "19132636353"
    send_whatsapp_message(test_number, "Hello from the echo bot!")
