import os

import click
from mikrokondo_tools.download import download as dwnld


options = {"gtdb-sketch": dwnld.Constants.sketch_url, 
        "dehost": dwnld.Constants.dehost_idx,
        "kraken-std": dwnld.Constants.kraken2_std,
        "bakta-light": dwnld.Constants.bakta_light,
        "bakta-full": dwnld.Constants.bakta_full}

@click.command(short_help="Download a database for mikrokondo", no_args_is_help=True)
@click.option("-f", "--file", "file", type=click.Choice(options.keys()), required = True, 
            help="Pick an option from the list to download")
@click.option("-o", "--output", "output", default=os.getcwd(), type=click.Path(), help="An existing directory to download files too.")
def download(file, output):
    """Download a external file for use in mikrokondo. This script only downloads the file and will not untar or unzip them.
    """
    option = options[file]
    dwnld.download_file(output_dir=output, url=option)