import module.cstat_handler as cstat_handler

import sys
from math import ceil
from pathlib import Path
from datetime import datetime


def main():
    if len(sys.argv) < 2:
        exit_general_usage()

    path_output_directory = Path(Path(__file__).parent.resolve(), "output")
    Path.mkdir(path_output_directory, exist_ok=True)

    if sys.argv[1].lower() == "collect":
        if len(sys.argv) < 3:
            exit_collect_usage(0)

        try:
            pages = round_pages(sys.argv[2])
        except (ValueError, IndexError):
            exit_collect_usage(-1)

        try:
            sort_order = sys.argv[3].lower()
        except (IndexError):
            sort_order = "points"
        
        if sort_order != "points" and sort_order != "time" and sort_order != "topdefender":
            exit_collect_sort_arg_error()

        # TODO: add custom output path option
        path_outfile = Path(path_output_directory, "cstat_data_" + (str(datetime.now()).replace(" ", "_")) + ".xlsx")
        print("Collecting", pages, "page(s) of cstat data sorted by", sort_order + "...")
        cstat_handler.scrape_and_export(pages, path_outfile, sort_order)
        print("Done.")
        exit(0)

    elif sys.argv[1].lower() == "compare":
        # TODO: verify files
        if len(sys.argv) < 3:
            exit_compare_usage(0)

        try:
            path_infile_old = Path(sys.argv[2]).resolve()
            path_infile_new = Path(sys.argv[3]).resolve()

        except (ValueError, IndexError):
            exit_compare_usage(-1)

        if not (path_infile_old.exists() and path_infile_new.exists()):
            exit_compare_file_error()

        # TODO: add custom output path option
        path_outfile = Path(path_output_directory, "cstat_diff_" + (str(datetime.now()).replace(" ", "_")) + ".xlsx")
        print("Comparing", path_infile_old, "and", str(path_infile_new) + "...")
        cstat_handler.find_cstat_diff(path_infile_old, path_infile_new, path_outfile)
        print("Done.")


def round_pages(arg: str) -> int:
    count = ceil(int(arg) / 15.0)
    if count < 0:
        raise ValueError
    return count


def exit_collect_usage(code: int):
    if code != 0: print("ERROR: improper arguments")
    print("Usage: python cstat.py collect [Number of cstat entries] [Sort criteria (default = points)]")
    print("Collects the specified number of cstat entries sorted according to the sort criteria and stores their associated data in an excel spreadsheet file (.xlsx).")
    print("Sort criteria include: points, time, topdefender")
    print("*Note: CSTAT entries are collected in multiples of 15.")
    print("*Note: Any input will be rounded to the next highest multiple of 15.")
    exit(code)


def exit_collect_sort_arg_error():
    print("ERROR: unrecognized sort criteria")
    print("Valid sort criteria are: points, time, topdefender")
    print("Usage: python cstat.py collect [Number of cstat entries] [Sort criteria (default = points)]")
    exit(-1)

def exit_compare_usage(code: int):
    if code != 0: print("ERROR: improper arguments")
    print("Usage: python cstat.py compare [Previous cstat data spreadsheet file] [Current cstat data spreadsheet file]")
    print("Computes the difference in cstat data statistics between entires recorded at two points in time, and outputs the result as an excel spreadsheet file (.xlsx).")
    print("*Note: CSTAT entries are only included in the output if entries for the same player exist in both inputs.")
    exit(code)


def exit_compare_file_error():
    print("ERROR: At least one file is inacessible or does not exist.")
    print("Usage: python cstat.py compare [Previous cstat data spreadsheet file] [Current cstat data spreadsheet file]")
    exit(-1)

def exit_general_usage():
    print("Usage: python cstat.py collect [Number of cstat entries]\n")
    print("Usage: python cstat.py compare [Previous cstat data spreadsheet file] [Current cstat data spreadsheet file]\n")
    print("Run \"python cstat.py collect\" or \"python cstat.py compare\" for more information.")
    exit(0)


if __name__ == "__main__":
    main()
