import time
import random
from instagrapi import Client, exceptions

USERNAME = "brokenboxpro"
PASSWORD = "Utanapishti543@"

# Rate limit settings
REQUESTS_PER_HOUR = 60  # Reduce this further to lower the risk of getting rate-limited
REQUEST_DELAY = 3600 / REQUESTS_PER_HOUR

client = Client()
client.login(USERNAME, PASSWORD)

hashtags = ["motivation", "tech"]
base_comments = [
    "Awesome post!",
    "Great content, please check @brokenboxpro",
    "Love this!",
    "Amazing work!",
    "Really inspiring!",
    "Keep it up!",
    "Fantastic job!",
    "This is so cool!",
    "Very informative!",
    "Thanks for sharing!"
]

# Additional elements to create more variations
emojis = ["😊", "👍", "🔥", "💯", "👏", "😍", "😎"]
extra_phrases = [
    "Well done!",
    "So true!",
    "Couldn't agree more!",
    "Absolutely!",
    "Wow, just wow!",
    "This is everything!",
    "Impressive!",
    "Really enjoyed this!",
    "Superb!",
    "On point!"
]

def generate_comment():
    comment = random.choice(base_comments)
    if random.random() > 0.5:  # Add an extra phrase about half the time
        comment += " " + random.choice(extra_phrases)
    if random.random() > 0.5:  # Add an emoji about half the time
        comment += " " + random.choice(emojis)
    return comment

def wait_if_needed(last_request_time, delay):
    elapsed = time.time() - last_request_time
    if elapsed < delay:
        time.sleep(delay - elapsed)

def like_comment_follow_media(media, comment_list, follow_probability=0.2):
    client.media_like(media.id)
    print(f"Liked post {media.id}")

    if random.random() < follow_probability:  # Follow based on probability
        client.user_follow(media.user.pk)
        print(f"Followed user {media.user.username}")

    comment = generate_comment()
    client.media_comment(media.id, comment)
    print(f"Commented '{comment}' under post {media.id}")

def handle_challenge(client, challenge):
    try:
        client.challenge_resolve(challenge)
    except exceptions.ChallengeRequired:
        print("Challenge resolution required. Please complete it manually.")

last_request_time = time.time()
delay_multiplier = 1

for hashtag in hashtags:
    print(f"Fetching posts for hashtag: {hashtag}")
    try:
        medias = client.hashtag_medias_recent(hashtag, 20)
    except Exception as e:
        print(f"Error fetching posts for hashtag {hashtag}: {e}")
        continue

    for i, media in enumerate(medias):
        try:
            wait_if_needed(last_request_time, REQUEST_DELAY * delay_multiplier)
            last_request_time = time.time()

            if hashtag == "programming":
                like_comment_follow_media(media, base_comments, follow_probability=0.5)
            else:
                like_comment_follow_media(media, base_comments, follow_probability=0.2)
            
            # Reset delay multiplier after a successful request
            delay_multiplier = 1

        except exceptions.ChallengeRequired as challenge:
            print(f"Challenge required for media {media.id}. Handling challenge.")
            handle_challenge(client, challenge)

        except Exception as e:
            print(f"Error processing media {media.id}: {e}")
            if "Please wait a few minutes before you try again" in str(e):
                # Exponential backoff
                delay_multiplier *= 2
                print(f"Increasing delay multiplier to {delay_multiplier}")
            else:
                # Handle other types of exceptions
                pass

            time.sleep(REQUEST_DELAY * delay_multiplier)

