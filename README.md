# What is this?

A small Telegram userbot (a program that acts under the name of an existing regular user account,
and not a ["Telegram bot"](https://core.telegram.org/bots)
(though nothing stops you from running it under a bot account
(aside form maybe message privacy settings)))
that replies with a "Good morning" to other "Good morning"s in a chat.

# Why?

Because the regular & repetitive emergence of "Good morning"s in the work chat screamed "automation" to me.
Plus I've wanted to mess around with Telegram's non-bot API for quite a while now.

# Setting it up

## Python

You will need Python 3.11+.

If you're a Windows user, [good luck](https://www.python.org/downloads/windows/)!

If you're a Linux user, just use your package manager. Unless they ship a Python version that is too old. In that case you can try [pyenv](https://github.com/pyenv/pyenv) ~~or updating/changing your distro~~.

Alternatively, you can just use Nix or Docker (more on that later).

## Pyrogram

You package manager is unlikely to ship pyrogram, so unless you want to use Nix or Docker (more on that later), you will have to install those manually.

Just use a venv!

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install pyrogram tgcrypto
```

If you're using some other shell than bash, then `source` the appropriate file from `venv/bin/`.
(On Windows the folder is instead named `venv/scripts/` for some reason? I think.)


## Nix or Docker

You can skip the previous two steps if you have nix or docker installed.

### Docker

For docker you will need docker-compose too. Then just
```shell
docker-compose up
```
### Nix

For nix you will need to enable flake support.

You can do this on per-command basis like this:
```shell
nix --experimental-features 'nix-command flakes' run
```

Or you can enable it persistently:
- On NixOS, [modify your system configuration](https://nixos.wiki/wiki/Flakes#NixOS).
- With Home-Manager, [modify *its* configuration](https://nixos.wiki/wiki/Flakes#Other_Distros:_With_Home-Manager).
- In other cases, modify your `~/.config/nix/nix.conf` or `/etc/nix/nix.conf` by adding
```
experimental-features = nix-command flakes
```

Then just
```
nix run
```

There's also a nix devShell (with pre-commit hooks) available,
```
nix develop
```

## Configuration

You will need a [Telegram "API_ID" and "API_HASH"](https://core.telegram.org/api/obtaining_api_id).

Copy the `config.example.toml` to `config.toml`.
Replace example values with your `api_id` and `api_hash`.
Set the ids or @usernames (enter them without the `@`)
of chats you want to run the userbot in.

Alternatively, you can pass `API_ID` & `API_HASH` as environment variables.
They take a higher priority than the ones in the config file.

You can change path to the configuration file by using `--config path/to/configuration/file.toml`
as an argument when launching the thing.

# Running it

```shell
python3 goodmorninguserbot.py
```

On the first launch you will need to log in or provide a bot token.
After that a `GoodMorning.session` file will be created in the current directory.
This file stores the login info, so you won't need to log in on the next run.
You won't have to provide `API_HASH` and `API_ID` after that either.

You can change the directory where this file will be stored and searched for:
use a `PYROGRAM_WORKDIR` environment variable or a `--pyrogram-workdir` command-line argument.
(Once again, the environment variable takes a higher priority).
