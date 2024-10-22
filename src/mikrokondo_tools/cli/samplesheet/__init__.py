import click
import pathlib as p
import errno as e
import sys

from mikrokondo_tools.samplesheet import samplesheet as ss
import mikrokondo_tools.utils as u

@click.command(short_help="Generate a sample sheet for mikrokondo.", no_args_is_help=True, context_settings={'show_default': True})
@click.option("-o", "--output-sheet", "output_sheet", required=True, type=click.Path(), help="The file to write your created output sheet to, this directory must already exist.")
@click.option("-1", "--read-1-suffix", "read_1", type=click.STRING, help="A suffix to identify read 1", default="_R1_")
@click.option("-2", "--read-2-suffix", "read_2", type=click.STRING, help="A suffix to identify read 2", default="_R2_")
@click.option("-s", "--schema-input", "schema_input", type=click.Path(), default=None, help="An optional schema_input.json file pre-downloaded for mikrokondo.")
@click.argument("input_directory", type=click.Path(exists=True))
def samplesheet(output_sheet, read_1, read_2, input_directory, schema_input):
    logger = u.get_logger(__name__)
    if output_sheet.is_file():
        logger.error("Input sample sheet already exists, please re-name your new sheet or the existing one. %s", output_sheet)
        sys.exit(e.EEXIST)

    data = ss.get_samples(p.Path(input_directory))
    ngs_data = ss.NGSData(data[0], data[1], read_1, read_2, p.Path(output_sheet), schema_input)
    return ngs_data.create_sample_sheet()