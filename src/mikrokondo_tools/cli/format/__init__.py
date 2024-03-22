import click

from mikrokondo_tools.format import format


@click.command(short_help='Format a nextflow_schema.json')
@click.option("-i", "--input", "file_input", type=click.Path(exists=True))
@click.option("-o", "--output", "output", type=click.Path(), help="Location to put updated json schema.")
def fmt(file_input, output):
    return format.reformat_schema(file_input, output)
