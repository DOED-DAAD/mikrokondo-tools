"""
tests for sketch downloading
"""

import pytest
import requests

from mikrokondo_tools.download import download


@pytest.mark.parametrize("uri",
                        [
                        (download.Constants.sketch_url),
                        (download.Constants.dehost_idx),
                        (download.Constants.kraken2_std),
                        (download.Constants.bakta_light),
                        (download.Constants.bakta_full)
                        ])
def test_constants_connection(uri):
    """Test URL connection is valid
    """
    with requests.get(uri, stream=True) as resp:
        assert resp.status_code == 200


@pytest.mark.parametrize( "input_url,value",
                        [("https://zenodo.org/records/8408361/files/GTDBSketch_20231003.msh",
                        "GTDBSketch_20231003.msh"),
                        ("https://zenodo.org/records/13969103/files/EnteroRef_GTDBSketch_20231003_V2.msh",
                        "EnteroRef_GTDBSketch_20231003_V2.msh"),
                        ("https://zenodo.org/records/8408557/files/PhiPacHum_m2.idx",
                        "PhiPacHum_m2.idx"),
                        ("https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz",
                        "k2_standard_20240112.tar.gz"),
                        ("https://zenodo.org/records/10522951/files/db-light.tar.gz",
                        "db-light.tar.gz"),
                        ("https://zenodo.org/records/10522951/files/db.tar.gz", "db.tar.gz"),
                        ("db.tar.gz", "db.tar.gz")
                        ])
def test_get_file_name(input_url, value):
    assert download.get_file_name(input_url) ==  value

