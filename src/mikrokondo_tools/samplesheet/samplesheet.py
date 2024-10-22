"""
Create a samplesheet for mikrokondo

Matthew Wells: 2024-10-21
"""
import json
import sys
from dataclasses import dataclass, asdict, fields
import pathlib as p
import typing as t
import errno as e

import jsonschema as js
import requests

import mikrokondo_tools.utils as u 

logger = u.get_logger(__name__)


__SCHEMA_INPUT_JSON__ = "https://raw.githubusercontent.com/phac-nml/mikrokondo/refs/heads/main/assets/schema_input.json"
__FASTA_EXTENSIONS__ = frozenset([".fa", ".fasta", ".fna"])
__FASTQ_EXTENSIONS__ = frozenset([".fastq", ".fq"])
__COMPRESSION_TYPES__ = frozenset([".gz"])


class DuplicateFilesException(Exception):
    pass

class MissingSchemaException(Exception):
    pass

@dataclass
class SampleRow:
    sample: str
    fastq_1: t.Optional[p.Path] = None
    fastq_2: t.Optional[p.Path] = None
    long_reads: t.Optional[p.Path] = None
    assembly: t.Optional[p.Path] = None

    def __getitem__(self, name: str) -> t.Union[str, p.Path, None] :
        return getattr(self, name)
    
    def __setitem__(self, key: str, value: str) -> None:
        setattr(self, key, value)

    def all_paths(self):
        return [self.fastq_1, self.fastq_2, self.long_reads, self.assembly]

    @classmethod
    def longreads_key(cls) -> str:
        #! Coupling with field name here
        return "long_reads"
    
    @classmethod
    def assembly_key(cls) -> str:
        #! Coupling with field name here
        return "assembly"

class NGSData:
    """
    Organization of ngs data for creation of a sample sheet
    """

    def __init__(self, reads: t.List[p.Path], fastas: t.List[p.Path], extension_r1: str, extension_r2: str, output_file: p.Path, json_schema: t.Optional[p.Path] = None):
        self.reads: t.List[str] = reads
        self.fastas: t.List[str] = fastas
        self.extension_r1: str = extension_r1
        self.extension_r2: str = extension_r2
        self.json_schema = self.get_json_schema(json_schema)
        self.output_file = output_file


    def get_json_schema(self, json_schema: p.Path):
        """
        Get the json schema to use
        """
        schema: dict = dict()
        if json_schema is not None:
            logger.info("Using schema path passed from command line %s", json_schema)
            with open(json_schema, 'r') as input_js:
                schema = json.load(input_js)
        else:
            logger.info("No json schema passed as an argument, downloading from: %s", __SCHEMA_INPUT_JSON__)
            try:
                schema = u.download_json(__SCHEMA_INPUT_JSON__, logger)
            except requests.HTTPError:
                logger.error("Could not download input schema nor was one passed to the program.")
                raise MissingSchemaException
        self._fix_pattern_regex(schema)
        return schema
    
    def _fix_pattern_regex(self, schema):
        """
        Incorporate empty string in pattern to allow for empty values
        """
        items_key: str = "items"
        properties_key: str = "properties"
        pattern_key: str = "pattern"
        for k, v in schema[items_key][properties_key].items():
            if pattern := v.get(pattern_key):
                pattern = rf"(?:{pattern}|^$)"
                schema[items_key][properties_key][k][pattern_key] = pattern

    def create_sample_sheet(self, sample_data: t.Optional[t.Dict[str, t.List[SampleRow]]] = None, output_file: t.Optional[p.Path] = None):
        """
        Main runner function to create a sample sheet
        """
        if sample_data is None:
            sample_data = self.organize_data()
        self.verify_unique_paths(sample_data)
        jsonified_data = self.jsonify_schema(sample_data)
        self.validate_json(jsonified_data)
        header = [i.name for i in fields(SampleRow)]

        if output_file is None:
            output_file = self.output_file

        if output_file.is_file():
            logger.error("Output file %s already exists.", str(output_file))
            raise e.EEXIST

        logger.info("Writing sample sheet to %s", str(output_file))
        with output_file.open("w") as output:
            output.write(f"{','.join(header)}\n")
            for data in jsonified_data:
                output.write(f"{','.join([data[text] for text in header])}\n") # Joining text to maintain order of fields



    
    def validate_json(self, jsonified_data: t.List[dict]):
        """
        Validate the json data
        """
        # Select correct Validator
        validator_class = js.validators.validator_for(self.json_schema)
        validator = validator_class(self.json_schema)
        errors = validator.iter_errors(jsonified_data)
        error_p = False
        for err in errors:
            error_p = True
            logger.error("Sample sheet validation error: %s", err.message)
        if error_p:
            raise js.ValidationError("Validation errors encountered check logs")
    
    def jsonify_schema(self, sample_data: t.Dict[str, t.List[SampleRow]]):
        """
        JSONify the sample data
        """
        samples_json: t.List[dict] = []
        for v in sample_data.values():
            for row in v:
                row_dict = asdict(row)
                for k, v in row_dict.items():
                    if v is None:
                        row_dict[k] = ""
                    elif isinstance(v, p.Path):
                        row_dict[k] = str(v)
                samples_json.append(row_dict)
        return samples_json

    def verify_unique_paths(self, samples: t.Dict[str, t.List[SampleRow]]):
        """
        Verify that all paths in the sample sheet are unique.
        """
        error = False
        paths: set[p.Path] = set()
        dup_paths: int = 0
        for k, v in samples.items():
            for rows in v:
                for path in rows.all_paths():
                    if path is None:
                        continue
                    if path in paths:
                        logger.error("Duplicate path listed in sample sheet for sample %s: %s this will cause an error.", k, path)
                        dup_paths += 1
                        error = True
                    else:
                        paths.add(path)
        if error:
            logger.error("%d duplicate paths identified see log for information.", dup_paths)
            raise DuplicateFilesException("Duplicate files found.")

    def organize_data(self) -> t.Dict[str, t.List[SampleRow]]:
        """
        Create the final sample sheet
        """
        pe_reads, se_reads, assemblies = self.get_ngs_data()
        sample_sheet: t.Dict[str, t.List[SampleRow]] = dict()

        for k, v in pe_reads.items():
            sample_sheet[k] = []
            for idx in range(len(v[0])):
                sample_sheet[k].append(SampleRow(sample=k, fastq_1=v[0][idx], fastq_2=v[1][idx]))

        self.update_sample_sheet_se(sample_sheet, se_reads.items(), SampleRow.longreads_key())
        self.update_sample_sheet_se(sample_sheet, assemblies.items(), SampleRow.assembly_key())
        return sample_sheet
    
    def update_sample_sheet_se(self, sample_sheet: t.Dict[str, t.List[SampleRow]], items: t.Iterable[t.Tuple[str, list]], field: str):
        for k, v in items:
            existing_data = sample_sheet.get(k)
            if existing_data:
                existing_data_len = len(existing_data)
                for idx, value in enumerate(v):
                    if idx < existing_data_len:
                        existing_data[idx][field] = value
                    else:
                        existing_data.append(SampleRow(sample=k, **{field: value}))
            else:
                sample_sheet[k] = []
                for ngs_data in v:
                    sample_sheet[k].append(SampleRow(sample=k, **{field: ngs_data}))

    def get_ngs_data(self) -> t.Tuple[t.Optional[t.Dict[str, t.Tuple[t.List[p.Path], t.List[p.Path]]]], t.Optional[t.Dict[str, t.List[p.Path]]], t.Optional[t.Dict[str, t.List[p.Path]]]]:
        """
        consolidate aggregate data into one data structure that can be validated
        """
        pe_reads: t.Optional[t.Dict[str, t.Tuple[t.List[p.Path], t.List[p.Path]]]] = None
        se_reads: t.Optional[t.Dict[str, t.List[p.Path]]] = None
        fastas: t.Optional[t.Dict[str, t.List[p.Path]]] = None

        if self.reads:
            pe_reads = self.get_paired_reads(self.reads)
            se_reads = self.get_sample_name_and_path(self.reads)
        if self.fastas:
            fastas = self.get_sample_name_and_path(self.fastas)
        if not self.fastas and not self.reads:
            logger.error("No input files found for processing.")
        return (pe_reads, se_reads, fastas)

    def get_paired_reads(self, reads: t.List[p.Path]) -> t.Dict[str, t.Tuple[t.List[p.Path], t.List[p.Path]]]:
        """
        Group the reads into bins of paired and unpaired reads
        """
        r1_reads: t.Dict[str, t.Tuple[t.List[p.Path], t.List[p.Path]]] = dict()
        
        for r in reads :
            if not r.match(f"**/*{self.extension_r1}*"):
                continue
            sample_name = r.name[:r.name.rfind(self.extension_r1)]
            if samples := r1_reads.get(sample_name):
                samples[0].append(r)
            else:
                r1_reads[sample_name] = ([r], [])

        r2_reads: t.List[t.Tuple[str, p.Path]] = [(r.name[:r.name.rfind(self.extension_r2)], r) for r in reads if r.match(f"**/*{self.extension_r2}*")]
        for r2 in r2_reads:
            if r1 := r1_reads.get(r2[0]):
                r1[1].append(r2[1])

        for k, v in r1_reads.items():
            if len(v[0]) != len(v[1]):
                logger.error("An un-even number of reads was identified for sample: %s", k)
                raise IndexError
        return r1_reads
    
    def get_sample_name_and_path(self, data: t.List[p.Path]) -> t.Dict[str, t.List[p.Path]]:
        """
        take single end reads or assemblies to return a list of tuples containing their contents
        """
        ngs_data: t.Dict[str, t.List[p.Path]] = dict()
        for i in data:
            if self.extension_r1 not in i.name and self.extension_r2 not in i.name:
                name = i.name[:i.name.index('.')]
                if data := ngs_data.get(name):
                    data.append(i)
                else:
                    ngs_data[name] = [i]
        return ngs_data

def get_schema_input(url: str) -> json:
    return u.download_json(url, logger)


def get_samples(directory: p.Path) -> t.Tuple[t.List[p.Path], t.List[p.Path]]:
    """
    Gather all sample information into one place for usage.

    directory Path: Path of sequence information
    """
    if not directory.is_dir():
        logger.error("Input directory does not exist or is not a directory: %s", directory)
        sys.exit(e.ENOENT)
    
    reads = []
    fastas = []

    for file in directory.iterdir():
        sfx = file.suffix
        if sfx in __COMPRESSION_TYPES__:
            try:
                sfx = file.suffixes[-2] # get second last file extension
            except IndexError:
                logger.error("File: %s is inappropriately no other extension is present besides %s", file, sfx)
                sys.exit(-1)
        if sfx in __FASTQ_EXTENSIONS__:
            reads.append(file.absolute())
        elif sfx in __FASTA_EXTENSIONS__:
            fastas.append(file.absolute())
        else:
            logger.warning("Miscellaneous file present in sample directory: %s", file)
    
    return reads, fastas

