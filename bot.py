import tweepy
import os
import time
import random
import shutil

# --- 1. API CREDENTIALS ---
# Replace these with your keys from the X Developer Portal
API_KEY = "1e5adG9bEOuNyGbpm6KcZVOyo"
API_SECRET = "JX2A_HBsuSA99BXD0dEyahefGLEi3RGQNLFIbWONSy9o1BjPTI"
ACCESS_TOKEN = "bDFDeU5mLWdrYTZhcnA2YjZtdFg6MTpjaQ"
ACCESS_SECRET = "MlYASNYJAawxS5drRmVWFWgKQku7MCYNCRZ8LVwCKuRmnEM77G"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAN1j7gEAAAAAz2OYlY2MFrTyr9yIfYMiltQ0EGY%3Dp84Cq5Fl5GPwWypJq46MVi9imRxF3dLkvjJReVgyYDMbg861Ty
"

# --- 2. CONFIGURATION ---
IMAGE_DIR = "./images"    # Folder with new images
POSTED_DIR = "./posted"  # Folder where used images go
CAPTIONS_FILE = "captions.txt"
INTERVAL = 9000  # 2.5 hours in seconds (9000s * 2 = 5 hours)

# Create posted directory if it doesn't exist
if not os.path.exists(POSTED_DIR):
    os.makedirs(POSTED_DIR)

# --- 3. AUTHENTICATION ---
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

def get_random_caption():
    try:
        with open(CAPTIONS_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        return random.choice(lines) if lines else "Melanie Martinez ✨"
    except FileNotFoundError:
        return "✨ #MelanieMartinez"

def post_content():
    # Get list of images
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    
    if not images:
        print("❌ No images left in the 'images' folder!")
        return False

    # Pick the first image (or use random.choice)
    image_name = images[0]
    image_path = os.path.join(IMAGE_DIR, image_name)
    caption = get_random_caption()

    try:
        # Upload media (v1.1 API required for media)
        media = api.media_upload(filename=image_path)
        
        # Post Tweet (v2 API)
        client.create_tweet(text=caption, media_ids=[media.media_id])
        
        # Move to 'posted' folder so it's not used again
        shutil.move(image_path, os.path.join(POSTED_DIR, image_name))
        
        print(f"✅ Successfully posted: {image_name}")
        return True
    except Exception as e:
        print(f"⚠️ Error occurred: {e}")
        return False

# --- 4. THE LOOP ---
print("Bot is starting... Press Ctrl+C to stop.")
while True:
    success = post_content()
    
    if success:
        # Adds a random 'jitter' of 1-10 minutes to look less like a bot
        jitter = random.randint(60, 600)
        wait_time = INTERVAL + jitter
        print(f"Next post in {wait_time // 60} minutes.")
        time.sleep(wait_time)
    else:
        # If folder is empty or error occurs, wait 10 mins and try again
        time.sleep(600)
