"""
Create a samplesheet for mikrokondo

Matthew Wells: 2024-10-21
"""
import json
import sys
from dataclasses import dataclass
import pathlib as p
import typing as t
import errno as e


import mikrokondo_tools.utils as u 

logger = u.get_logger(__name__)


__SCHEMA_INPUT_JSON__ = "https://raw.githubusercontent.com/phac-nml/mikrokondo/refs/heads/main/assets/schema_input.json"
__FASTA_EXTENSIONS__ = frozenset([".fa", ".fasta", ".fna"])
__FASTQ_EXTENSIONS__ = frozenset([".fastq", ".fq"])
__COMPRESSION_TYPES__ = frozenset([".gz"])


@dataclass
class SampleRow:
    sample: str
    fastq_1: t.Optional[p.Path] = None
    fastq_2: t.Optional[p.Path] = None
    long_reads: t.Optional[p.Path] = None
    assembly: t.Optional[p.Path] = None

class NGSData:
    """
    Organization of ngs data for creation of a sample sheet
    """

    def __init__(self, reads: list[p.Path], fastas: list[p.Path], extension_r1: str, extension_r2: str):
        self.reads: list[str] = reads
        self.fastas: list[str] = fastas
        self.extension_r1: str = extension_r1
        self.extension_r2: str = extension_r2

    def create_sample_sheet(self):
        """
        Create the final sample sheet
        """
        pe_reads, se_reads, assemblies = self.get_ngs_data()
        sample_sheet: dict[str, list[SampleRow]] = dict()

        for k, v in pe_reads.items():
            sample_sheet[k] = []
            for idx in range(len(v[0])):
                sample_sheet[k].append(SampleRow(sample=k, fastq_1=v[0][idx], fastq_2=v[1][idx]))

        
        # TODO tommorrow seperate this into a different function and add the option to incorporate assemblies
        for k, v in se_reads.items():
            existing_data = sample_sheet.get(k)
            if existing_data:
                existing_data_len = len(existing_data)
                for idx, value in enumerate(v):
                    if existing_data_len < idx:
                        existing_data[idx].long_reads = value
                    else:
                        existing_data.append(SampleRow(sample=k, long_reads=value))
            else:
                sample_sheet[k] = []
                for ngs_data in v:
                    sample_sheet[k].append(SampleRow(sample=k, long_reads=ngs_data))


    def get_ngs_data(self) -> tuple[t.Optional[dict[str, tuple[list[p.Path], list[p.Path]]]], t.Optional[dict[str, list[p.Path]]], t.Optional[dict[str, list[p.Path]]]]:
        """
        consolidate aggregate data into one data structure that can be validated
        """
        pe_reads: t.Optional[dict[str, tuple[list[p.Path], list[p.Path]]]] = None
        se_reads: t.Optional[dict[str, list[p.Path]]] = None
        fastas: t.Optional[dict[str, list[p.Path]]] = None

        if self.reads:
            pe_reads = self.get_paired_reads(self.reads)
            se_reads = self.get_sample_name_and_path(self.reads)
        if self.fastas:
            fastas = self.get_sample_name_and_path(self.fastas)
        if not self.fastas and not self.reads:
            logger.error("No input files found for processing.")
        return (pe_reads, se_reads, fastas)

    def get_paired_reads(self, reads: list[p.Path]) -> dict[str, tuple[list[p.Path], list[p.Path]]]:
        """
        Group the reads into bins of paired and unpaired reads
        """
        r1_reads: dict[str, tuple[list[p.Path], list[p.Path]]] = dict()
        
        for r in reads :
            if not r.match(f"**/*{self.extension_r1}*"):
                continue
            sample_name = r.name[:r.name.rfind(self.extension_r1)]
            if samples := r1_reads.get(sample_name):
                samples[0].append(r)
            else:
                r1_reads[sample_name] = ([r], [])

        r2_reads: list[tuple[str, p.Path]] = [(r.name[:r.name.rfind(self.extension_r2)], r) for r in reads if r.match(f"**/*{self.extension_r2}*")]
        for r2 in r2_reads:
            if r1 := r1_reads.get(r2[0]):
                r1[1].append(r2[1])

        for k, v in r1_reads.items():
            if len(v[0]) != len(v[1]):
                logger.error("An un-even number of reads was identified for sample: %s", k)
                raise IndexError
        return r1_reads
    
    def get_sample_name_and_path(self, data: list[p.Path]) -> dict[str, list[p.Path]]:
        """
        take single end reads or assemblies to return a list of tuples containing their contents
        """
        ngs_data: dict[str, list[p.Path]] = dict()
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


def get_samples(directory: p.Path) -> tuple[list[p.Path], list[p.Path]]:
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

