#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Number Base Converter.

This module returns a formatted string of the input converted to various bases.
"""

import sys
import re
import dataclasses

@dataclasses.dataclass
class _Style:
    """Enumerable for formatting codes."""

    BOLDU  = "\033[1;4m"
    PLAIN  = "\033[0m"
    RED    = "\033[31;1m"
    PURPLE = "\033[35;1m"
    BLUE   = "\033[34;1m"
    YELLOW = "\033[93;1m"


def ParseAndExecute(values : str) -> str:
    """Separate command line values and pass to the main function of the module."""

    collated_result = [fmt for fmt in
                       [FormatOtherTypes(x) for x in values]
                       if fmt]

    return "\n".join(collated_result)


def FormatOtherTypes(value : str):
    """
    Convert the input string to an integer based on base notation and return
    the in various bases.
    """

    founds = re.findall(pattern=r"^\d+$|0?[oxdb]?\d+$|^\d+[ohdb]?$",string=value)

    if len(founds) != 1:
        # not a number. raise ValueError
        return None

    # should only ever be 1 in regular usage
    found = founds[0]
    # need to tolerate leading zero formatters, e.b. 0bXXXX
    numerals = re.findall(pattern=r"^(\d+)$|0?[oxdb]?(\d+)$|^(\d+)[ohdb]?$",string=found)[0]
    numerals = [n for n in numerals if n][0]

    base10 = None
    if "d" in found:
        base10 = int(numerals)
    elif "h" in found or "x" in found:
        base10 = int(f"0x{numerals}",16)
    elif "o" in found:
        base10 = int(f"0o{numerals}",8)
    elif "b" in found:
        base10 = int(f"0b{numerals}",2)
    else:
        # assume already base 10
        base10 = int(numerals)

    collection = [
        f"{_Style.BOLDU}Input: {value}{_Style.PLAIN}",
        f"\n{_Style.PURPLE}Hexadecimal{_Style.PLAIN}: {base10:02x}",
        f"{' '*4}{_Style.BLUE}Decimal{_Style.PLAIN}: {base10:d}",
        f"{' '*4}{_Style.YELLOW}Octal{_Style.PLAIN}: {base10:o}",
        f"{' '*4}{_Style.RED}Binary{_Style.PLAIN}: {base10:04b}",
        ]

    return "".join(collection)

#########################
#   Running as main     #
#########################

if __name__ == "__main__":
    print(ParseAndExecute(sys.argv[1:]))