# mikrokondo_tools

[![PyPI - Version](https://img.shields.io/pypi/v/mikrokondo-tools.svg)](https://pypi.org/project/mikrokondo-tools)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mikrokondo-tools.svg)](https://pypi.org/project/mikrokondo-tools)

-----

# Note

## This repo is underdevelopment and not ready for routine usage

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

### Installation from PIP

The easiest way to install the repository is from pip by running the following command.

```
pip install mikrokondo-tools
```

### Installation from conda

```
conda install mikrokondo-tools -c bioconda
```


### Installation Instructions for Developers

No package has been created yet, however the software can be run and developed using `hatch`. To run the tests in all supported python versions using hatch simply enter:
```
hatch run test:test
```

To run tests using a specific python version use:

```
# Example running using python 3.10
hatch run +py=3.10 test:test
```

To run the command-line options use:

```
hatch run +py=3.10 test:mikrokondo-tools
```

The above command will display command groups with help messages, and each sub command has additional help options.

This option can be used to create a developer install from the source repository.

```console
pip install -e mikrokondo-tools
```

## Usage

Running `mikrokondo-tools` generates the following help message with available options for usage:

```
Usage: mikrokondo-tools [OPTIONS] COMMAND [ARGS]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  download     Download a database for mikrokondo
  samplesheet  Generate a sample sheet for mikrokondo.
```

The `download` option generates the following output:

```
Usage: mikrokondo-tools download [OPTIONS]

  Download a external file for use in mikrokondo. This script only downloads
  the file and will not untar or unzip them.

Options:
  -f, --file [gtdb-sketch|gtdb-shigella|dehost|kraken-std|bakta-light|bakta-full]
                                  Pick an option from the list to download
                                  [required]
  -o, --output PATH               An existing directory to download files to.
                                  [default: your/current/directory]
  -h, --help                      Show this message and exit.
```

The `samplesheet` command can be used to create and validate sample sheet from a directory of NGS data. The `schema_input.json` file is downloaded directly from the main mikrokondo repository each time so this utility will update with the pipeline. You can still pass a pre-existing `schema_input.json` file to the utility if you do not have internet access or you are using an older version of the pipeline that is no longer supported.

The `samplesheet` option produces the following output:

```
Usage: mikrokondo-tools samplesheet [OPTIONS] SAMPLE_DIRECTORY

Options:
  -o, --output-sheet PATH   The file to write your created output sheet to,
                            this directory must already exist.  [required]
  -1, --read-1-suffix TEXT  A suffix to identify read 1  [default: _R1_]
  -2, --read-2-suffix TEXT  A suffix to identify read 2  [default: _R2_]
  -s, --schema-input PATH   An optional schema_input.json file pre-downloaded
                            for mikrokondo.
  -h, --help                Show this message and exit.
```


## License

Copyright Government of Canada 2023

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
