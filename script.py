from instagrapi import Client
import time
from instagrapi.exceptions import PleaseWaitFewMinutes
import requests  # Import requests module for handling HTTP errors

def login_with_2fa(username, password):
    client = Client()
    try:
        client.login(username, password)
        print("Logged in successfully!")
    except client.exceptions.TwoFactorRequired:
        verification_code = input("Enter the two-factor authentication code: ")
        try:
            client.login(username, password, verification_code=verification_code)
            print("Logged in successfully after entering verification code!")
        except client.exceptions.InvalidVerificationCode as e:
            print(f"Invalid verification code: {e}")
        except client.exceptions.InstagramException as e:
            print(f"Failed to login after entering verification code: {e}")
    except client.exceptions.BadPassword as e:
        print(f"Invalid password: {e}")
    except client.exceptions.InstagramException as e:
        print(f"Failed to login: {e}")

def search_hashtag(client, hashtag):
    retry_delay = 10  # Initial retry delay in seconds
    max_retries = 5   # Maximum number of retry attempts

    for attempt in range(max_retries):
        try:
            results = client.search_hashtags(hashtag)
            if results:
                print(f"Results for #{hashtag}:")
                for post in results:
                    print(post)
            else:
                print(f"No results found for #{hashtag}.")
            return  # Exit the function if successful
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print(f"Unauthorized error: {e}")
                return  # No need to retry on authorization error
            elif e.response.status_code == 429:
                print(f"Rate limit exceeded. Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
                retry_delay *= 2
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"HTTP error searching hashtag '{hashtag}': {e}")
                return  # Exit on other HTTP errors
        except PleaseWaitFewMinutes as e:
            print(f"Rate limit exceeded. Waiting {retry_delay} seconds before retrying...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        except client.exceptions.InstagramException as e:
            print(f"Instagram API error searching hashtag '{hashtag}': {e}")
            return  # Exit on other Instagram API errors

    print(f"Maximum retry attempts ({max_retries}) exceeded. Exiting.")
    return

if __name__ == "__main__":
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")

    # Login with two-factor authentication support
    login_with_2fa(username, password)

    # Initialize the client after successful login
    client = Client()
    try:
        # Example usage: searching hashtags
        hashtags = ["dailymotivation", "motivation", "programming", "technology"]
        for hashtag in hashtags:
            search_hashtag(client, hashtag)

    except KeyboardInterrupt:
        print("\nOperation interrupted.")
    finally:
        # Optionally logout when done with operations
        client.logout()
