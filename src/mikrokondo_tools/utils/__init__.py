"""
Utility programs for mikrokondo tools

Matthew Wells: 2024-10-21
"""

import sys
import logging
import json

import requests

def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    return logging.getLogger(name)


def download_json(url: str, logger: logging.Logger) -> json:
    """
    Download a *small* json file into a string to be returned
    """

    logger.info("Downloading data: %s", url)
    with requests.get(url, stream=True) as resp:
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            logger.error("Could not access: %s", url)
            sys.exit(requests.HTTPError)
        else:
            return json.loads(rf"{resp.text}")
