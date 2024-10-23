# SPDX-FileCopyrightText: 2024-present Matthew Wells <mattwells9@shaw.ca>
#
# SPDX-License-Identifier: MIT
import sys
import traceback
import mikrokondo_tools.utils as u

if __name__ == "__main__":
    #from mikrokondo_tools.cli import mikrokondo_tools
    from mikrokondo_tools.cli import main
    logger = u.get_logger(__name__)
    
    try:
        main()
    except Exception as e:
        errors_out = "errors.txt"
        logger.warning("Error encountered appending traceback to %s", errors_out)
        with open(errors_out, 'r') as output:
            output.write(traceback.format_exc())
        error_number = e.errno if hasattr(e, "errno") else -1
        SystemExit(error_number)
    else:
        logger.info("Program finished.")

    sys.exit(-1)
