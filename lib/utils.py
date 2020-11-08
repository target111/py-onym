from argparse import ArgumentTypeError
from typing import Tuple, Dict, Optional

from asyncio.streams import StreamReader
import json
import time
import random
import re

PROXY_REGEX = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$"

def encode_to_bytes(data: str or bytes) -> bytes:
    """
    Simple helper function that ensures that data is encoded to `bytes` as UTF-8
    :param data: takes in both `str` or `bytes` object; represents any type of string or bytes object
    :return: utf-8 encoded bytes object
    """
    return data if isinstance(data, bytes) else data.encode('utf-8')


def decode_to_string(data: str or bytes) -> str:
    """
    Simple helper function that ensures that data is decoded from `bytes` with `UTF-8` encoding scheme
    :param data: takes in both `str` or `bytes` object; represents any type of string or bytes object
    :return: string object
    """
    return data if isinstance(data, str) else data.decode('utf-8')


async def read_from_json(reader: StreamReader) -> Optional[Dict]:
    length = int.from_bytes(await reader.read(2), byteorder='big')
    if not length:
        return None

    data = await reader.read(length)

    try:
        return json.loads(decode_to_string(data))
    except Exception:
        raise ValueError(f'An error occurred while parsing JSON.')


def sleep_random(*duration: Tuple[float, float]) -> None:
    """
    sleep_random is designed to emulate a human user by pausing execution of the
    program (sleeping) for a random duration of time between `a` and `b` seconds.
    :param duration: tuple containing two floats: `a` is the minimum sleep duration while `b` is the maximum duration
    """
    a: float = 0
    b: float = 0
    try:
        a, b = duration
    except ValueError as e:
        print(e)
    sleep_time = random.uniform(a, b)
    print(f'Pausing execution flow for {sleep_time} seconds...')
    time.sleep(sleep_time)

def proxy_regex(proxy_arg: str, pat=re.compile(PROXY_REGEX)):
    if not pat.match(proxy_arg):
        raise ArgumentTypeError(f"invalid proxy value: '{proxy_arg}'")
    return proxy_arg
