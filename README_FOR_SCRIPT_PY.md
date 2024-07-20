# Instagram Hashtag Search Bot

This repository contains an Instagram bot that can log in using two-factor authentication (2FA) and search for posts based on specified hashtags. It includes error handling for login issues, rate limiting, and HTTP errors.

## Features

- Supports login with two-factor authentication (2FA).
- Searches for posts using specified hashtags.
- Handles various errors including rate limiting and HTTP errors.

## Requirements

- Python 3.7+
- `instagrapi` library for interacting with the Instagram API.
- `requests` library for handling HTTP errors.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your Instagram credentials:**

   Ensure you have your Instagram username and password ready for login.

## Usage

1. **Run the bot:**

    ```bash
    python instagram_hashtag_search_bot.py
    ```

2. **How the bot works:**

    - Prompts the user to enter Instagram credentials.
    - Logs into Instagram using the provided credentials and handles 2FA if required.
    - Searches for posts using specified hashtags and prints the results.

## Configuration

- **Hashtags:**

  You can customize the hashtags the bot searches for in the script:

    ```python
    hashtags = ["dailymotivation", "motivation", "programming", "technology"]
    ```

## How It Works

1. **Login with Two-Factor Authentication:**

    The bot attempts to log in with the provided username and password. If 2FA is required, it prompts the user to enter the verification code.

    ```python
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
    ```

2. **Search Hashtags:**

    The bot searches for posts using specified hashtags and handles various errors, including rate limiting with exponential backoff.

    ```python
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
    ```

3. **Run the Bot:**

    The main function initializes the client, logs in with 2FA support, and searches for posts using specified hashtags.

    ```python
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
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions, feel free to reach out to [Sandrowest501@outlook.com](mailto:sandrowest501@outlook.com).
