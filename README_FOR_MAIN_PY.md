# Instagram Automation Bot

This repository contains an Instagram automation bot that likes, comments, and optionally follows users based on specified hashtags. The bot is designed to interact with posts in a randomized and human-like manner to reduce the risk of getting rate-limited or banned by Instagram.

## Features

- Likes posts based on specified hashtags.
- Leaves random comments on posts.
- Optionally follows users based on a probability setting.
- Handles Instagram challenges that may arise during automation.

## Requirements

- Python 3.7+
- `instagrapi` library for interacting with the Instagram API.

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

   Create a `config.py` file and add your Instagram username and password:

    ```python
    USERNAME = 'your_instagram_username'
    PASSWORD = 'your_instagram_password'
    ```

## Usage

1. **Run the automation bot:**

    ```bash
    python instagram_bot.py
    ```

2. **How the bot works:**

    - The bot logs into your Instagram account using the credentials provided in `config.py`.
    - It fetches recent posts for the specified hashtags.
    - For each post, the bot likes the post, leaves a randomized comment, and optionally follows the user based on a predefined probability.
    - The bot handles Instagram challenges that may arise during automation to ensure smooth operation.

## Configuration

- **Rate Limit Settings:**

  You can adjust the rate limit settings to control how frequently the bot interacts with posts:

    ```python
    REQUESTS_PER_HOUR = 60  # Number of requests per hour
    REQUEST_DELAY = 3600 / REQUESTS_PER_HOUR  # Delay between requests in seconds
    ```

- **Hashtags and Comments:**

  You can customize the hashtags the bot searches for and the comments it leaves:

    ```python
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
    ```

## How It Works

1. **Generate Comments:**

    The bot generates comments by randomly combining base comments, extra phrases, and emojis to create variations.

    ```python
    def generate_comment():
        comment = random.choice(base_comments)
        if random.random() > 0.5:  # Add an extra phrase about half the time
            comment += " " + random.choice(extra_phrases)
        if random.random() > 0.5:  # Add an emoji about half the time
            comment += " " + random.choice(emojis)
        return comment
    ```

2. **Wait Between Requests:**

    The bot waits between requests to avoid getting rate-limited by Instagram.

    ```python
    def wait_if_needed(last_request_time, delay):
        elapsed = time.time() - last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)
    ```

3. **Like, Comment, and Follow:**

    The bot likes posts, leaves comments, and optionally follows users based on a probability setting.

    ```python
    def like_comment_follow_media(media, comment_list, follow_probability=0.2):
        client.media_like(media.id)
        print(f"Liked post {media.id}")

        if random.random() < follow_probability:  # Follow based on probability
            client.user_follow(media.user.pk)
            print(f"Followed user {media.user.username}")

        comment = generate_comment()
        client.media_comment(media.id, comment)
        print(f"Commented '{comment}' under post {media.id}")
    ```

4. **Handle Challenges:**

    The bot handles Instagram challenges that may arise during automation.

    ```python
    def handle_challenge(client, challenge):
        try:
            client.challenge_resolve(challenge)
        except exceptions.ChallengeRequired:
            print("Challenge resolution required. Please complete it manually.")
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions, feel free to reach out to [Sandrowest501@outlook.com](mailto:Sandrowest501@outlook.com).
