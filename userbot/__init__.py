import asyncio
import datetime
import logging
import os
import random
import re

from pyrogram import Client, enums, filters, types

from . import config

GOOD_MORNING_REGEXP = re.compile(r"[Дд]оброе +утро[\.!]*")
GOOD_MORNING_TEXT = "Доброе утро"


client = Client(
    name="GoodMorning",
    api_id=config.api_id,
    api_hash=config.api_hash,
    workdir=os.getenv("PYROGRAM_WORKDIR", Client.WORKDIR),
)


def get_threshold(chat_id: int, date: datetime.date) -> int:
    # Insert your threshold selection logic here
    return random.randint(1, 4)


_last_dates: dict[int, datetime.date] = {}
_counts: dict[int, int] = {}
_thresholds: dict[int, int] = {}


@client.on_message(
    filters=filters.regex(GOOD_MORNING_REGEXP) & filters.chat(config.chats)
)
async def good_morning_handler(client: Client, message: types.Message):
    logging.info("Good morning received: %s", repr(message))
    chat_id: int = message.chat.id
    today: datetime.date = datetime.date.today()
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
        logging.info(f"Time for a {GOOD_MORNING_TEXT!r}!")
        await client.read_chat_history(chat_id, message.id)
        await asyncio.sleep(3)
        await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
        logging.info("Started typing...")
        await asyncio.sleep(3)
        result = await message.reply(GOOD_MORNING_TEXT, quote=False)
        logging.info(f"{GOOD_MORNING_TEXT}! {result!r}")
        await client.read_chat_history(chat_id, message.id)
