# mikrokondo_tools

[![PyPI - Version](https://img.shields.io/pypi/v/mikrokondo-tools.svg)](https://pypi.org/project/mikrokondo-tools)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mikrokondo-tools.svg)](https://pypi.org/project/mikrokondo-tools)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

### Current Run Method

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

Console installation has not been tested.
```console
pip install mikrokondo-tools
```

## License

Copyright Government of Canada 2023

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
