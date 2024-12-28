import requests,os
from dotenv import load_dotenv
# Replace with your bot token and chat ID
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_text_message(message):
    """Send a text message to the user."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Text message sent successfully!")
    else:
        print(f"Failed to send text message: {response.status_code}")
        print(response.json())

def send_image_message(image_path, caption=None):
    """Send an image with an optional caption to the user."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as image_file:
        files = {"photo": image_file}
        data = {"chat_id": CHAT_ID, "caption": caption}
        response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        print("Image sent successfully!")
    else:
        print(f"Failed to send image: {response.status_code}")
        print(response.json())

# Example usage
if __name__ == "__main__":
    send_text_message("Hello, this is a text notification!")
    send_image_message("example.jpg", caption="Here is an image!")
