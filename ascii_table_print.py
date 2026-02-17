#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""ASCII Table Print.

This module provides a formatted ASCII table.

This module should be run from the command line or called with ParseAndExecute.
"""

import argparse
import dataclasses
from io import StringIO

#########################
#      Enumerables      #
#########################

@dataclasses.dataclass
class CodeType:
    """Enumerable for formatting output based on type."""

    CONTROL   = 0x00
    SYMBOL    = 0x01
    NUMBER    = 0x02
    CHARACTER = 0x03

@dataclasses.dataclass
class TypeStyle:
    """Enumerable for formatting codes."""

    PLAIN  = "\033[0m"
    BOLD_U = "\033[1;4m"
    BOLD   = "\033[1m"
    RED    = "\033[31;1m"
    INV    = "\033[7m"
    PURP   = "\033[35m"
    BLUE   = "\033[34m"
    YELW   = "\033[93;1m"

@dataclasses.dataclass
class Spacing:
    """Enumerable for formatting codes."""

    PARTS   = "  "
    COLUMNS = "    "


#########################
#        Mapping        #
#########################

class _CodeRangeMapping():

    def __init__(self, start : int, end : int, codetype : CodeType):
        self.Start = start
        self.End   = end
        self.Type  = codetype

        self.Range = list(range(self.Start, self.End))


#########################
#      Formatters       #
#########################

def _FormatControlString(controlcode : int,
                         shortstring : str,
                         description : str,
                         hexonly : bool = False,
                         ) -> str:
    """Take an control code (integer) and output a formatted string.

    Formats an integer to a string displaying the numerical value, the short
    code, and the name of the cotrol function.
    """
    string_hex = f"{controlcode:02X}{TypeStyle.PURP}h{TypeStyle.PLAIN}"
    string_dec = f"{controlcode:03}{TypeStyle.BLUE}d{TypeStyle.PLAIN}"
    string_ctrl = f"{TypeStyle.BOLD}{shortstring:<3}{TypeStyle.PLAIN}"
    string_desc = f"{description:<20}\t"

    string_list = [
        string_hex,
        string_dec,
        string_ctrl,
        string_desc,
        ]

    if hexonly:
        string_list.remove(string_dec)

    return Spacing.PARTS.join(string_list)


def _FormatOutputString(asciivalue : int,
                       codetype : CodeType,
                       hexonly : bool = False
                       ) -> str:
    """Take an integer and output a formatted string.

    Formats an integer to a string displaying the numerical value and as a
    printable character using console colour highlighting.
    """
    string_hex = f"{asciivalue:02X}{TypeStyle.PURP}h{TypeStyle.PLAIN}"
    string_dec = f"{asciivalue:03}{TypeStyle.BLUE}d{TypeStyle.PLAIN}"

    style_list = [
        f"{chr(asciivalue)}", # control
        f"{chr(asciivalue)}", # symbol
        f"{TypeStyle.RED}{chr(asciivalue)}{TypeStyle.PLAIN}", # number
        f"{TypeStyle.YELW}{chr(asciivalue)}{TypeStyle.PLAIN}", # character
        ]
    string_chr = style_list[codetype]

    string_list = [
        string_hex,
        string_dec,
        string_chr,
        ]

    if hexonly:
        string_list.remove(string_dec)

    return Spacing.PARTS.join(string_list)


#########################
#    Output strings     #
#########################

def _GetControls(hexonly : bool = False) -> str:
    codes = {
        "NUL" : "Null character",
        "SOH" : "Start of Heading",
        "STX" : "Start of Text",
        "ETX" : "End of Text",
        "EOT" : "End of Transmission",
        "ENQ" : "Enquiry",
        "ACK" : "Acknowledge",
        "BEL" : "Bell, Alert",
        "BS"  : "Backspace",
        "HT"  : "Horizontal Tab",
        "LF"  : "Line Feed",
        "VT"  : "Vertical Tabulation",
        "FF"  : "Form Feed",
        "CR"  : "Carriage Return",
        "SO"  : "Shift Out",
        "SI"  : "Shift In",
        "DLE" : "Data Link Escape",
        "DC1" : "Device Control One (XON)",
        "DC2" : "Device Control Two",
        "DC3" : "Device Control Three (XOFF)",
        "DC4" : "Device Control Four",
        "NAK" : "Negative Acknowledge",
        "SYN" : "Synchronous Idle",
        "ETB" : "End of Transmission Block",
        "CAN" : "Cancel",
        "EM"  : "End of medium",
        "SUB" : "Substitute",
        "ESC" : "Escape",
        "FS"  : "File Separator",
        "GS"  : "Group Separator",
        "RS"  : "Record Separator",
        "US"  : "Unit Separator",
        }

    arr = [_FormatControlString(i, key, codes[key], hexonly=hexonly)
                                               for i,key in enumerate(codes)]

    rows = 16
    cols = 2
    stringified = StringIO()
    for row in range(rows):
        stringified.write(" " + Spacing.COLUMNS.join(arr[row:row+(rows*cols):rows]).rstrip())
        stringified.write("\n")

    stringified = stringified.getvalue()

    # invert "printable" codes
    highlights = ["BS", "CR", "LF", "HT"]
    for light in highlights:
        stringified = stringified.replace(f"{light}", f"{TypeStyle.INV}{light}{TypeStyle.PLAIN}")

    return stringified


def _GetPrintables(hexonly : bool = False) -> str:
    """Output: printable characters formatted with hexadecimal and decimal values."""
    style_ranges = [
            _CodeRangeMapping(0x20, 0x30, CodeType.SYMBOL),
            _CodeRangeMapping(0x30, 0x3A, CodeType.NUMBER),
            _CodeRangeMapping(0x3A, 0x41, CodeType.SYMBOL),
            _CodeRangeMapping(0x41, 0x5B, CodeType.CHARACTER),
            _CodeRangeMapping(0x5B, 0x61, CodeType.SYMBOL),
            _CodeRangeMapping(0x61, 0x7B, CodeType.CHARACTER),
            _CodeRangeMapping(0x7B, 0x7F, CodeType.SYMBOL),
        ]

    combined =sum([[_FormatOutputString(i, s.Type, hexonly=hexonly)
                                for i in s.Range] for s in style_ranges],[])

    rows = 16
    cols = 6
    stringified = ""
    for row in range(rows):
        stringified += " " + Spacing.COLUMNS.join(combined[row:row+(rows*cols):rows])
        stringified += "\n"

    return stringified


#########################
#   Primary functions   #
#########################

def GetTable(args : dict = None) -> None:
    """Print the ASCII character and code map."""
    pseudo_string_builder = StringIO()
    if args["full"] or args["controlonly"]:
        pseudo_string_builder.write(f"\n{TypeStyle.BOLD_U}Control Codes{TypeStyle.PLAIN}\n")
        pseudo_string_builder.write(_GetControls(args["hexonly"]))
    if not args["controlonly"]:
        pseudo_string_builder.write(f"\n{TypeStyle.BOLD_U}Printable Characters{TypeStyle.PLAIN}\n")
        pseudo_string_builder.write(_GetPrintables(args["hexonly"]))

    return pseudo_string_builder.getvalue()


def ParseAndExecute() -> str:
    """
    Parse command line arguments and execute the main function of the module.

    To list output options, run with the -h or --help flag.
    """
    parser = argparse.ArgumentParser(
        prog="ASCII Table",
        description="Prints the ASCII table mapping."
        )

    parser.add_argument("-c",
                        "--controlonly",
                        help="Only print details of control codes.",
                        action="store_true")

    parser.add_argument("-f",
                        "--full",
                        help="Include control codes in printout.",
                        action="store_true")

    parser.add_argument("-s",
                        "--slim",
                        help="Use slim spacing for printable character table",
                        action="store_true")

    parser.add_argument("-x",
                        "--hexonly",
                        help="Do not print decimal values.",
                        action="store_true")


    command_line_args = vars(parser.parse_args())

    if command_line_args["slim"]:
        Spacing.PARTS   = " "
        Spacing.COLUMNS = "  "
    else:
        Spacing.PARTS   = "  "
        Spacing.COLUMNS = "    "

    return GetTable(command_line_args)

#########################
#   Running as main     #
#########################

if __name__ == "__main__":
    print(ParseAndExecute())
