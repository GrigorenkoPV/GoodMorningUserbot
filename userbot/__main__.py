import logging
import os
import random

from . import client

logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
    ],
    level=os.getenv("LOGLEVEL", "INFO").upper(),
    format="[%(asctime)s.%(msecs)03d] [%(name)s] [%(levelname)s]: %(message)s",
    datefmt=r"%Y-%m-%dT%H-%M-%S",
)

random.seed()
client.run()
