# What is this?

A small Telegram userbot (a program that acts under the name of an existing regular user account,
and not a ["Telegram bot"](https://core.telegram.org/bots)
(though nothing stops you from running it under a bot account
(aside form maybe message privacy settings)))
that replies with a "Good morning" to other "Good mornings" in a chat.

# Why?

Because the repetitive morning routine of being nice gave me an idea that it might be possible to automate it. Plus I've wanted to mess around with Telegram's non-bot API for quite a while now.

# How to run it?

0. You will need python (probably 3.10+ because I've used some fancy type annotations).
And [dependencies](requirements.txt) installed.
(Hint: use [venv](https://docs.python.org/3/library/venv.html))
1. You will need a [Telegram "API_ID" and "API_HASH"](https://core.telegram.org/api/obtaining_api_id). And a willingness to potentially sacrifice your Telegram account because I've heard multiple stories of users unfairly receiving bans from Telegram for using userbots even without any malicious intent. Alternatively, you can run this under a bot account.
2. Copy the `config.example.py` to `config.py`.
Replace example values with your `api_id` and `api_hash`.
Set the ids or @usernames (enter them without the `@`)
of chats you want to run the userbot in.
3. On the first launch you will need to log in. After that a `Something-something.session` file will be created and it will store the login info, so you won't need to log in again. If you want to just login, without launching the userbot, run `login.py` or `login.sh` (the latter set ups a venv automatically and runs the former).
4. Launch the userbot with `python -m userbot` or `python userbot.py` or `./service/launch.sh` (the latter automatically sets up a venv).
5. ?????
6. That's it. You can also run this as a systemd service, see [here](service).
