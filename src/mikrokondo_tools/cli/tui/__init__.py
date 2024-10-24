
import click

from mikrokondo_tools.tui.tui import tui as tui_generator

@click.command(short_help="tui")
def tui():
    tui_generator()