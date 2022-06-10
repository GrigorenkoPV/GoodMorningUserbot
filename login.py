#!/usr/bin/env python3

from telethon import TelegramClient

import config

TelegramClient(
    session=config.session_name,
    api_id=config.api_id,
    api_hash=config.api_hash,
).start()
