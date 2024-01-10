import time
import requests
import json
from keep_alive import keep_alive

keep_alive()

# Twitch API credentials
client_id = '5vbnkp6tjtk9o2jy4kr9li372ja4dm'
client_secret = '4uzclx2q4bxyfdz6oszymyrh8ckkjs'

# Twitch streamer to check
streamer = 'Sweetbuttcheeks'

# Discord webhook URL
webhook_url = 'https://discord.com/api/webhooks/1194732995324694588/flaW6OEgej-Sf1gK1FwLzHoRtZYehLThOK8YOxmWI6es7h3CDv3iU907kdR8vnfRQAOa'

# Function to get Twitch API access token
def get_twitch_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=payload)
    return response.json()['access_token']

# Function to check if a streamer is online
def is_online(streamer, client_id, token):
    url = f'https://api.twitch.tv/helix/streams?user_login={streamer}'
    headers = {'Client-ID': client_id, 'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.json()['data'] != []

# Function to send a message to Discord
def send_discord_message(content, webhook_url):
    data = {'content': content}
    response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    return response.status_code

# Get Twitch API access token
token = get_twitch_token(client_id, client_secret)

# Main loop
while True:
    if is_online(streamer, client_id, token):
        if not message_sent:
            send_discord_message(f'@Everyone {streamer} is now live on Twitch!', webhook_url)
            message_sent = True
    else:
        message_sent = False  # Reset the flag when the streamer is offline
    time.sleep(60)  # Check every minute
