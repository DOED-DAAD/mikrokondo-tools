"""
Download sketches from zenodo

Matthew Wells: 2024-04-18
"""
import requests

import logging
import itertools
import sys
import os
from dataclasses import dataclass


logging.basicConfig(stream=sys.stderr, level=logging.INFO) # TODO this should probably go somewhere else
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Constants:
    sketch_url: str = "https://zenodo.org/records/8408361/files/GTDBSketch_20231003.msh"
    dehost_idx: str = "https://zenodo.org/records/8408557/files/PhiPacHum_m2.idx"
    kraken2_std: str = "https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz"
    bakta_light: str = "https://zenodo.org/records/10522951/files/db-light.tar.gz"
    bakta_full: str = "https://zenodo.org/records/10522951/files/db.tar.gz"
    chunk_size: int = 8192


def get_file_name(input_uri: str) -> str:
    """Get the file name from the URL
    input_uri str: return the file name from the passed in URI
    """
    return input_uri.split("/")[-1]

def download_file(url: str, output_dir: str = None) -> str:
    """Download a file from zenodo and put it in the correct output director
    
    output_dir str|os.Path: Output location different then local directory
    """
    output_file = get_file_name(url)
    if output_dir and os.path.isdir(output_dir):
        output_file = os.path.join(output_dir, output_file)

    spinner = itertools.cycle(["-", "/", "|", "\\"])

    logger.info("Downloading %s to %s", url, output_file)
    with requests.get(url, stream=True) as resp:
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            logger.error("Could not access: %s and update maybe required", url)
            sys.exit(-1)
        else:
            logger.info("Beginning download, this may take some time.")
            with open(output_file, 'wb') as out:
                for chunk in resp.iter_content(chunk_size=Constants.chunk_size):
                    out.write(chunk)
                    sys.stdout.write(next(spinner))
                    sys.stdout.flush()
                    sys.stdout.write('\b')
    return output_file
