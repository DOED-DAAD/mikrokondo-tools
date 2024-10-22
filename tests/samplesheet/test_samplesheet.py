"""
Test for sample sheet generation

Matthew Wells: 2024-10-21
"""

import pytest
import pathlib as p
from dataclasses import asdict
import jsonschema as js

import mikrokondo_tools.samplesheet.samplesheet as ss

def test_get_samples():
    """
    Test the get samples from the directory
    """
    ngs_samples = ss.get_samples(p.Path("tests/samplesheet/data"))
    assert len(ngs_samples[0]) == 6
    assert len(ngs_samples[1]) == 2

@pytest.fixture()
def ngs_data_fail(tmp_path):
    sample_data = ss.get_samples(p.Path("tests/samplesheet/data"))
    return ss.NGSData(sample_data[0], sample_data[1], "_r1", "_r2", tmp_path / "output.csv")

@pytest.fixture()
def ngs_data_pass(tmp_path):
    sample_data = ss.get_samples(p.Path("tests/samplesheet/data"))
    return ss.NGSData(sample_data[0], sample_data[1], "_r1_", "_r2_", tmp_path / "output.csv")

def test_get_paired_reads_fails(ngs_data_fail):
    with pytest.raises(IndexError):
        ngs_data_fail.get_paired_reads(ngs_data_fail.reads)

def test_get_paired_reads_pass(ngs_data_pass):
    keys = ngs_data_pass.get_paired_reads(ngs_data_pass.reads).keys()
    assert list(keys) == ['s1']


def test_get_se(ngs_data_pass):
    reads = ngs_data_pass.get_sample_name_and_path(ngs_data_pass.reads)
    assert [i for i in reads] == ["s1", "s2_r1"]
    fastas = ngs_data_pass.get_sample_name_and_path(ngs_data_pass.fastas)
    assert [i for i in fastas] == ["s1", "s3"]


def test_organize_data(ngs_data_pass):
    ss_out = ngs_data_pass.organize_data()
    outputs = {
    "s1": [ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_dup.fq.gz'), fastq_2=p.Path('s1_r2_.fq.gz'), long_reads=p.Path('s1.fq.gz'), assembly=p.Path('s1.fa.gz')), 
        ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_.fq.gz'), fastq_2=p.Path('s1_r2_dup.fq.gz'), long_reads=None, assembly=None)], 
    
    "s2_r1": [ss.SampleRow(sample='s2_r1', fastq_1=None, fastq_2=None, long_reads=p.Path('s2_r1.fq'), assembly=None)], 
    
    "s3": [ss.SampleRow(sample='s3', fastq_1=None, fastq_2=None, long_reads=None, assembly=p.Path('s3.fa'))]}
    assert len(ss_out) == 3, "Inequal number of keys in sample data sheet"
    assert outputs.keys() == ss_out.keys(), "Key sets differ"
    for k, v in outputs.items():
        sample_rows = ss_out[k]
        assert len(v) == len(sample_rows)
        for i, f in zip(sample_rows, v):
            sample_data = asdict(f)
            for field in sample_data:
                if field is None:
                    assert i[field] is None
                elif isinstance(i[field], p.Path):
                    assert sample_data[field].stem == i[field].stem # Comparing file names only
                else:
                    assert sample_data[field] == i[field]

def test_verify_unique_paths(ngs_data_pass):
    outputs = {
        "s1": [ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_dup.fq.gz'), fastq_2=p.Path('s1_r2_.fq.gz'), long_reads=p.Path('s1.fq.gz'), assembly=p.Path('s1.fa.gz')), 
            ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_.fq.gz'), fastq_2=p.Path('s1_r2_dup.fq.gz'), long_reads=None, assembly=None),
            ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_.fq.gz'), fastq_2=p.Path('s1_r2_dup.fq.gz'), long_reads=None, assembly=None)], 
        
        "s2_r1": [ss.SampleRow(sample='s2_r1', fastq_1=None, fastq_2=None, long_reads=p.Path('s2_r1.fq'), assembly=None)], 
        
        "s3": [ss.SampleRow(sample='s3', fastq_1=None, fastq_2=None, long_reads=None, assembly=p.Path('s3.fa'))]}
    with pytest.raises(ss.DuplicateFilesException):
        ngs_data_pass.verify_unique_paths(outputs)

def test_validate_json_pass(ngs_data_pass):
    outputs = {
        "s1": [ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_dup.fq.gz'), fastq_2=p.Path('s1_r2_.fq.gz'), long_reads=p.Path('s1.fq.gz'), assembly=p.Path('s1.fa.gz')), 
            ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_.fq.gz'), fastq_2=p.Path('s1_r2_dup.fq.gz'), long_reads=None, assembly=None)], 
        "s2_r1": [ss.SampleRow(sample='s2_r1', fastq_1=None, fastq_2=None, long_reads=p.Path('s2_r1.fq.gz'), assembly=None)], 
        "s3": [ss.SampleRow(sample='s3', fastq_1=None, fastq_2=None, long_reads=None, assembly=p.Path('s3.fa.gz'))]}
    json_data = ngs_data_pass.jsonify_schema(outputs)
    ngs_data_pass.validate_json(json_data)


def test_fail_json_validation_fail(ngs_data_pass):
    outputs = {
    "s1": [ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_dup.fq.gz'), fastq_2=p.Path('s1_r2_.fq.gz'), long_reads=p.Path('s1.fq.gz'), assembly=p.Path('s1.fa.gz')), 
        ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_.fq.gz'), fastq_2=p.Path('s1_r2_dup.fq.gz'), long_reads=None, assembly=None)], 
    "s2_r1": [ss.SampleRow(sample='s2_r1', fastq_1=None, fastq_2=None, long_reads=p.Path('s2_r1.fq.gz'), assembly=None)], 
    "s3": [ss.SampleRow(sample='s3', fastq_1=None, fastq_2=None, long_reads=None, assembly=p.Path('s3.fa.gz'))],
    "s4": [ss.SampleRow(sample='s4', fastq_1=None, fastq_2=None, long_reads=None, assembly=p.Path('s4.fa'))],
    "s5": [ss.SampleRow(sample='s5', fastq_1=None, fastq_2=None, long_reads=None, assembly=p.Path('st.fa'))]}
    json_data_fail = ngs_data_pass.jsonify_schema(outputs)
    with pytest.raises(js.ValidationError):
        ngs_data_pass.validate_json(json_data_fail)


def test_create_sample_sheet(ngs_data_pass, tmp_path):
    outputs = {
        "s1": [ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_dup.fq.gz'), fastq_2=p.Path('s1_r2_.fq.gz'), long_reads=p.Path('s1.fq.gz'), assembly=p.Path('s1.fa.gz')), 
            ss.SampleRow(sample='s1', fastq_1=p.Path('s1_r1_.fq.gz'), fastq_2=p.Path('s1_r2_dup.fq.gz'), long_reads=None, assembly=None)], 
        "s2_r1": [ss.SampleRow(sample='s2_r1', fastq_1=None, fastq_2=None, long_reads=p.Path('s2_r1.fq.gz'), assembly=None)], 
        "s3": [ss.SampleRow(sample='s3', fastq_1=None, fastq_2=None, long_reads=None, assembly=p.Path('s3.fa.gz'))]}
    output = tmp_path / "output_sheet.csv"
    ngs_data_pass.create_sample_sheet(outputs, output)