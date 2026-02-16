import tweepy
import os
import random
import shutil

# --- API CREDENTIALS (Using Environment Variables for security) ---
API_KEY = os.environ.get("CONSUMER_KEY")
API_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

IMAGE_DIR = "./images"
POSTED_DIR = "./posted"
CAPTIONS_FILE = "captions.txt"

# Ensure posted directory exists
os.makedirs(POSTED_DIR, exist_ok=True)

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY, consumer_secret=API_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET)

def post_one():
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not images:
        print("No images left!")
        return

    image_name = images[0]
    image_path = os.path.join(IMAGE_DIR, image_name)

    with open(CAPTIONS_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    caption = random.choice(lines) if lines else "Melanie Martinez ✨"

    try:
        media = api.media_upload(filename=image_path)
        client.create_tweet(text=caption, media_ids=[media.media_id])
        shutil.move(image_path, os.path.join(POSTED_DIR, image_name))
        print(f"Posted {image_name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    post_one()
