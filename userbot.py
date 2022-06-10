#!/usr/bin/env python3

import datetime
import logging
import os
import random
import re

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

import config

GOOD_MORNING_REGEXP = re.compile(r"[Дд]оброе +утро[\.!]*")
GOOD_MORNING_TEXT = "Доброе утро"

logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
    ],
    level=os.getenv("LOGLEVEL", "INFO").upper(),
    format="[%(asctime)s.%(msecs)03d] [%(name)s] [%(levelname)s]: %(message)s",
    datefmt=r"%Y-%m-%dT%H-%M-%S",
)


def get_threshold(chat_id: int, date: datetime.date) -> int:
    # Insert your threshold selection logic here
    return random.randint(1, 5)


client: TelegramClient = TelegramClient(
    session=config.session_name,
    api_id=config.api_id,
    api_hash=config.api_hash,
)


def get_today() -> datetime.date:
    # Insert your timezone logic here
    return datetime.date.today()


def is_good_morning(message: Message) -> bool:
    text = message.text
    match = GOOD_MORNING_REGEXP.fullmatch(message.text)
    logging.debug(f"The match for {text!r} is {match}")
    return bool(match)


_last_dates: dict[int, datetime.date] = {}
_counts: dict[int, int] = {}
_thresholds: dict[int, int] = {}


@client.on(events.NewMessage(chats=config.chats))
async def good_morning_handler(event: events.NewMessage.Event):
    logging.debug(f"New event: {event}")
    chat_id: int = event.chat_id
    message: Message = event.message
    if not is_good_morning(message):
        return
    logging.info(f"Good morning received: {message}")
    today: datetime.date = get_today()
    last_date: datetime.date | None = _last_dates.get(chat_id)
    logging.debug(f"Previous good morning was received on {last_date}")
    if last_date is None or last_date < today:
        logging.debug("First good morning of the day, setting up things...")
        _last_dates[chat_id] = today
        _counts[chat_id] = 1
        _thresholds[chat_id] = get_threshold(chat_id, today)
    else:
        _counts[chat_id] = _counts[chat_id] + 1
    count = _counts[chat_id]
    threshold = _thresholds[chat_id]
    logging.info(f"This is good morning #{count}/{threshold}")
    if count == threshold:
        await message.respond(GOOD_MORNING_TEXT)
        await client.send_read_acknowledge(event.chat_id)


with client:
    client.run_until_disconnected()
