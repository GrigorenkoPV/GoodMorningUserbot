import argparse
import asyncio
import datetime
import logging
import os
import random
import re
import tomllib
from dataclasses import dataclass

from pyrogram import Client, enums, filters, handlers, types

logger = logging.getLogger(__name__)

GOOD_MORNING_REGEXP = re.compile(r"[Дд]оброе +утро[\.!]*$", re.MULTILINE)
GOOD_MORNING_TEXT = "Доброе утро"


def get_threshold(chat_id: int, date: datetime.date) -> int:
    # Insert your threshold selection logic here
    return random.randint(1, 4)


@dataclass
class ChatInfo:
    last_date: datetime.date | None
    count: int
    threshold: int


ChatId = int
chats: dict[ChatId, ChatInfo] = {}


async def good_morning_callback(client: Client, message: types.Message):
    logger.info("Good morning received: %s", repr(message))
    chat_id: ChatId = message.chat.id
    today: datetime.date = datetime.date.today()
    chat_info = chats.setdefault(
        chat_id, ChatInfo(last_date=None, count=0, threshold=0)
    )
    last_date = chat_info.last_date
    logger.debug(f"Previous good morning was received on {chat_info}")
    if last_date is None or last_date < today:
        logger.debug("First good morning of the day, setting things up...")
        chat_info.last_date = today
        chat_info.count = 1
        chat_info.threshold = get_threshold(chat_id, today)
    else:
        chat_info.count += 1
    count = chat_info.count
    threshold = chat_info.threshold
    logger.info(f"This is good morning #{count}/{threshold}")
    if count == threshold:
        logger.info(f"Time for a {GOOD_MORNING_TEXT!r}!")
        await client.read_chat_history(chat_id, message.id)
        await asyncio.sleep(3)
        await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
        logger.info("Started typing...")
        await asyncio.sleep(3)
        result = await message.reply(GOOD_MORNING_TEXT, quote=False)
        logger.info(f"{GOOD_MORNING_TEXT}! {result!r}")
        await client.read_chat_history(chat_id, message.id)


def construct_client(api_id, api_hash, workdir, chats) -> Client:
    client = Client(
        name="GoodMorning",
        api_id=api_id,
        api_hash=api_hash,
        workdir=workdir,
    )
    client.add_handler(
        handlers.MessageHandler(
            filters=filters.regex(GOOD_MORNING_REGEXP) & filters.chat(chats),
            callback=good_morning_callback,
        )
    )
    return client


def main():
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(),
        ],
        level=os.getenv("LOGLEVEL", "INFO").upper(),
        format="[%(asctime)s.%(msecs)03d] [%(name)s] [%(levelname)s]: %(message)s",
        datefmt=r"%Y-%m-%dT%H-%M-%S",
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pyrogram-dir",
        default=".",
        help="the directory where the session files are stored",
    )
    parser.add_argument(
        "--config",
        default="config.toml",
        help="path to the configuration file",
    )
    args = parser.parse_args()
    with open(args.config, "rb") as f:
        config = tomllib.load(f)

    client = construct_client(
        api_id=os.getenv("API_ID", config.get("api_id")),
        api_hash=os.getenv("API_HASH", config.get("api_hash")),
        workdir=os.getenv("PYROGRAM_WORKDIR", args.pyrogram_dir),
        chats=config["chats"],
    )
    random.seed()
    client.run()


if __name__ == "__main__":
    import sys

    sys.exit(main())
