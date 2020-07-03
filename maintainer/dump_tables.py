#! /usr/bin/env python3

"""This script dumps the F1 2020 telemetry tables in ReST or MarkDown format."""

import os
import sys
import argparse

# Make sure we import from the f1_2020_telemetry package inside the repository.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..')))

from f1_2020_telemetry.packets import PacketID, TeamIDs, DriverIDs, TrackIDs, NationalityIDs, SurfaceTypes, ButtonFlag, EventStringCode

def dump_table_rst(items, labels, num_rows=None, num_cols=None):
    """Dump a number of items as an ReST markup table.

    Args:
        items: a sequence of n-element items, to ne included in the table body.
        labels: an optional sequence of n strings to be used as headers.
        num_rows: number of rows to be used. Defaults to the length of the 'items' sequence.
        num_cols: number of 'major' columns (each consisting of n 'minor' columns).
    """

    if num_rows is None:
        num_rows = len(items)

    if num_cols is None:
        num_cols = (len(items) + num_rows - 1) // num_rows

    labels = [str(label) for label in labels]
    items  = [tuple(str(x) for x in item) for item in items]

    # Determine column widths
    column_widths = []
    for col in range(num_cols):
        widths = (len(x) for x in labels)
        for row in range(num_rows):
            idx = num_rows * col + row
            if idx < len(items):
                widths = tuple(max(w, len(x)) for (w, x) in zip(widths, items[idx]))
        column_widths.append(widths)

    # Ready to print

    separator_line_1 = "+" + "+".join("+".join((w + 2) * "-" for w in widths) for widths in column_widths) + "+"
    separator_line_2 = "+" + "+".join("+".join((w + 2) * "=" for w in widths) for widths in column_widths) + "+"

    print(separator_line_1)

    if labels is not None:
        print("|", end='')
        for (col, widths) in enumerate(column_widths):
            for (label, width) in zip(labels, widths):
                print(" " + label + (width - len(label) + 1) * " ", end='')
                print("|", end='')
        print()

        print(separator_line_2)

    for row in range(num_rows):

        print("|", end='')
        for (col, widths) in enumerate(column_widths):
            idx = num_rows * col + row
            values = items[idx] if idx < len(items) else ("", "")
            for (value, width) in zip(values, widths):
                print(" " + value + (width - len(value) + 1) * " ", end='')
                print("|", end='')
        print()

        print(separator_line_1)


def dump_table_markdown(items, labels, num_rows=None, num_cols=None):
    """Dump a number of items as a MarkDown table.

    Args:
        items: a sequence of n-element items, to ne included in the table body.
        labels: an optional sequence of n strings to be used as headers.
        num_rows: number of rows to be used. Defaults to the length of the 'items' sequence.
        num_cols: number of 'major' columns (each consisting of n 'minor' columns).
    """

    if num_rows is None:
        num_rows = len(items)

    if num_cols is None:
        num_cols = (len(items) + num_rows - 1) // num_rows

    labels = [str(label) for label in labels]
    items  = [tuple(str(x) for x in item) for item in items]

    # Determine column widths
    column_widths = []
    for col in range(num_cols):
        widths = (len(x) for x in labels)
        for row in range(num_rows):
            idx = num_rows * col + row
            if idx < len(items):
                widths = tuple(max(w, len(x)) for (w, x) in zip(widths, items[idx]))
        column_widths.append(widths)

    # Ready to print

    separator_line_1 = "|" + "|".join("|".join(" " + w * "-" + " " for w in widths) for widths in column_widths) + "|"

    if labels is not None:
        print("|", end='')
        for (col, widths) in enumerate(column_widths):
            for (label, width) in zip(labels, widths):
                print(" " + label + (width - len(label) + 1) * " ", end='')
                print("|", end='')
        print()

        print(separator_line_1)

    for row in range(num_rows):

        print("|", end='')
        for (col, widths) in enumerate(column_widths):
            idx = num_rows * col + row
            values = items[idx] if idx < len(items) else ("", "")
            for (value, width) in zip(values, widths):
                print(" " + value + (width - len(value) + 1) * " ", end='')
                print("|", end='')
        print()


def dump_tables(dump_table_func):

    # This table is in the spec as given on the CodeMaster forum, but not in the module.
    # Note that we added the 'uint32' type which is missing from the spec.
    TypesAndDescriptionsTable = [
        ( "uint8_t"  , "Unsigned 8-bit integer"  ),
        ( "int8_t"   , "Signed 8-bit integer"    ),
        ( "uint16_t" , "Unsigned 16-bit integer" ),
        ( "int16_t"  , "Signed 16-bit integer"   ),
        ( "uint32_t" , "Unsigned 32-bit integer" ),
        ( "float"    , "Floating point (32-bit)" ),
        ( "uint64_t" , "Unsigned 64-bit integer" )
    ]

    dump_table_func(TypesAndDescriptionsTable, ["Type", "Description"])
    print()

    PacketIDTable = [(PacketID.short_description[p], p.value, PacketID.long_description[p]) for p in PacketID]
    dump_table_func(PacketIDTable, ["Packet Name", "Value", "Description"])
    print()

    EventStringCodeTable = [(EventStringCode.short_description[e], e.value.decode(), EventStringCode.long_description[e]) for e in EventStringCode]
    dump_table_func(EventStringCodeTable, ["Event", "Code", "Description"])
    print()

    dump_table_func(sorted(TeamIDs.items()), ["ID", "Team"], 20)
    print()

    dump_table_func(sorted(DriverIDs.items()), ["ID", "Driver"], 30)
    print()

    dump_table_func(sorted(TrackIDs.items()), ["ID", "Track"])
    print()

    dump_table_func(sorted(NationalityIDs.items()), ["ID", "Nationality"], 30)
    print()

    dump_table_func(sorted(SurfaceTypes.items()), ["ID", "Surface"])
    print()

    ButtonFlagTable = [("0x{:04x}".format(k), v) for (k, v) in sorted((bf.value, ButtonFlag.description[bf]) for bf in ButtonFlag)]
    dump_table_func(ButtonFlagTable, ["Bit flags", "Button"])
    print()


def main():
    """Dump F1 2020 tables in ReST or MarkDown format."""

    argparser = argparse.ArgumentParser

    parser = argparse.ArgumentParser(description='Dump F1 2020 tables in format suitable for documentation.')
    parser.add_argument('-f', '--format', default='rst', choices=['rst', 'markdown'],
                        help='Format of tables to be dumped (default: rst).')

    args = parser.parse_args()

    if args.format == 'rst':
        dump_table_func = dump_table_rst
    else:
        dump_table_func = dump_table_markdown

    dump_tables(dump_table_func)


if __name__ == "__main__":
    main()
