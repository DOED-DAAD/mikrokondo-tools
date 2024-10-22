# SPDX-FileCopyrightText: 2024-present Matthew Wells <mattwells9@shaw.ca>
#
# SPDX-License-Identifier: MIT
import click

from mikrokondo_tools.__about__ import __version__
from mikrokondo_tools.cli.download import download
from mikrokondo_tools.cli.format import fmt
from mikrokondo_tools.cli.samplesheet import samplesheet


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True, no_args_is_help=True)
@click.version_option(version=__version__, prog_name="mikrokondo_tools")
def mikrokondo_tools():
    pass

mikrokondo_tools.add_command(fmt)
mikrokondo_tools.add_command(download)
mikrokondo_tools.add_command(samplesheet)



def main():
    return mikrokondo_tools(prog_name='mikrokondo-tools')
