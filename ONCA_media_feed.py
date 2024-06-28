import feedparser
import pandas as pd
import os
from datetime import datetime
import requests


# pushover
api_token = os.getenv("PUSHOVER_API_TOKEN")
user_key = os.getenv("PUSHOVER_USER_KEY")
pushover_url = "https://api.pushover.net/1/messages.json"

def send_notification(message, api_token=api_token, user_key=user_key, pushover_url=pushover_url):
    data = {
        "token": api_token,
        "user": user_key,
        "message": message,
    }

    response = requests.post(pushover_url, data=data)
    if response.status_code != 200:
        sys.exit('Failed to send notification. Exiting script.')

# RSS feed

url = 'https://www.ontariocourts.ca/rss/coa/media.xml'

feed = feedparser.parse(url)

if len(feed['entries']):
    send_notification(f"New media feed entry: {feed['entries'][0]['title']}")
    
    # check if there is a media folder
    if not os.path.exists('ONCA_media'):
        os.mkdir('ONCA_media')
        
    # check if there is a master.csv file
    if not os.path.exists('ONCA_media/master.csv'):
        df = pd.DataFrame(feed['entries'])
        df.to_csv('ONCA_media/master.csv', index=False)
    
    else:
        df = pd.read_csv('ONCA_media/master.csv')
        number_of_entries = len(df)
        df = pd.concat([df, pd.DataFrame(feed['entries'])], ignore_index=True)
        df = df.drop_duplicates(subset=['id'])
        new_number_of_entries = len(df)
        
        if new_number_of_entries > number_of_entries:
            df.to_csv('ONCA_media/master.csv', index=False)

