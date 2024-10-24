# SPDX-FileCopyrightText: 2024-present Matthew Wells <mattwells9@shaw.ca>
#
# SPDX-License-Identifier: MIT
import click

import traceback
import mikrokondo_tools.utils as u

from mikrokondo_tools.__about__ import __version__
from mikrokondo_tools.cli.download import download
from mikrokondo_tools.cli.samplesheet import samplesheet
from mikrokondo_tools.cli.tui import tui


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True, no_args_is_help=True)
@click.version_option(version=__version__, prog_name="mikrokondo_tools")
def mikrokondo_tools():
    pass

mikrokondo_tools.add_command(download)
mikrokondo_tools.add_command(samplesheet)
mikrokondo_tools.add_command(tui)


def safe_entry_point():
    logger = u.get_logger(__name__)
    try:
        mikrokondo_tools(prog_name='mikrokondo-tools')
    except Exception as e:
        errors_out = "errors.txt"
        logger.warning("Error encountered appending traceback to %s for debugging.", errors_out)
        with open(errors_out, 'a') as output:
            output.write(traceback.format_exc())
        error_number = e.errno if hasattr(e, "errno") else -1
        SystemExit(error_number)
    else:
        logger.info("Program finished.")

def main():
    return safe_entry_point

