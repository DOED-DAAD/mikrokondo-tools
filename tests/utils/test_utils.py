import pytest

import mikrokondo_tools.utils as u 



def test_download_json(real_input_schema):
    """
    Test the request method for downloading json
    """
    test_logger = u.get_logger(__name__)
    output = u.download_json("https://raw.githubusercontent.com/phac-nml/mikrokondo/refs/heads/main/assets/schema_input.json", test_logger)  
    assert output == real_input_schema