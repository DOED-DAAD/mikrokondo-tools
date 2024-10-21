"""
Test for sample sheet generation

Matthew Wells: 2024-10-21
"""

import pytest
import pathlib as p

import mikrokondo_tools.samplesheet.samplesheet as ss



def test_get_samples():
    """
    Test the get samples from the directory
    """
    ngs_samples = ss.get_samples(p.Path("tests/samplesheet/data"))
    assert len(ngs_samples[0]) == 4
    assert len(ngs_samples[1]) == 2

@pytest.fixture()
def ngs_data_fail():
    sample_data = ss.get_samples(p.Path("tests/samplesheet/data"))
    return ss.NGSData(sample_data[0], sample_data[1], "_r1", "_r2")

@pytest.fixture()
def ngs_data_pass():
    sample_data = ss.get_samples(p.Path("tests/samplesheet/data"))
    return ss.NGSData(sample_data[0], sample_data[1], "_r1_", "_r2_")

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


def test_create_sample_sheet(ngs_data_pass):
    ngs_data_pass.create_sample_sheet()