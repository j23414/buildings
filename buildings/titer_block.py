#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import xlrd
from collections import defaultdict
import re

def parse_args():
    parser = argparse.ArgumentParser(
        description="Find the block of titers in an Excel worksheet.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--file",
                        default="~/nextstrain/fludata/VIDRL-Melbourne-WHO-CC/raw-data/A/H1N1pdm/HI/2024/20240528H1N1.xlsx",
                        required=False,
                        help="Path to the Excel file")
    return parser.parse_args()

def is_numeric(value):
    """
    Check if the value is numeric or a string representing a numeric value with '<'.

    Basically checking for titer values e.g. "80", "< 10", "1400", etc.
    """
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        value = value.strip()
        if value.startswith('<'):
            try:
                float(value[1:].strip())
                return True
            except ValueError:
                return False
    return False

def find_titer_block(worksheet):
    """
    Find the block of titers in the worksheet.

    To reduce false positives, the function looks for rows and columns where at least two consecutive cells contain numeric values.
    """
    col_start_dict = defaultdict(int)
    col_end_dict = defaultdict(int)
    row_start_dict = defaultdict(int)
    row_end_dict = defaultdict(int)

    # Iterate over each row
    for row_idx in range(worksheet.nrows):
        first_numeric_index = None
        last_numeric_index = None
        for col_idx in range(worksheet.ncols):
            cell_value = worksheet.cell_value(row_idx, col_idx)
            next_cell_value = worksheet.cell_value(row_idx, col_idx + 1) if col_idx + 1 < worksheet.ncols else None

            # Check for two consecutive numeric values in a row before incrementing the count
            if is_numeric(cell_value) and is_numeric(next_cell_value):
                if first_numeric_index is None:
                    first_numeric_index = col_idx
                last_numeric_index = col_idx + 1

        # Only increment if any numeric values were found in the row
        if first_numeric_index is not None:
            col_start_dict[first_numeric_index] += 1
            col_end_dict[last_numeric_index] += 1

    # Iterate over each column
    for col_idx in range(worksheet.ncols):
        first_numeric_index = None
        last_numeric_index = None
        for row_idx in range(worksheet.nrows):
            cell_value = worksheet.cell_value(row_idx, col_idx)
            next_cell_value = worksheet.cell_value(row_idx + 1, col_idx) if row_idx + 1 < worksheet.nrows else None

            # Check for two consecutive numeric values in a column before incrementing the count
            if is_numeric(cell_value) and is_numeric(next_cell_value):
                if first_numeric_index is None:
                    first_numeric_index = row_idx
                last_numeric_index = row_idx + 1

        # Only increment if any numeric values were found in the column
        if first_numeric_index is not None:
            row_start_dict[first_numeric_index] += 1
            row_end_dict[last_numeric_index] += 1
    
    # Sort the dictionaries by frequency in descending order
    sorted_col_start = sorted(col_start_dict.items(), key=lambda item: item[1], reverse=True)
    sorted_col_end = sorted(col_end_dict.items(), key=lambda item: item[1], reverse=True)
    sorted_row_start = sorted(row_start_dict.items(), key=lambda item: item[1], reverse=True)
    sorted_row_end = sorted(row_end_dict.items(), key=lambda item: item[1], reverse=True)

    return {
        "col_start": sorted_col_start,
        "col_end": sorted_col_end,
        "row_start": sorted_row_start,
        "row_end": sorted_row_end,
    }

def find_strain_column(worksheet, col_start, row_end):
    """
    Find the column containing strain names based on the most likely column indices for the titer block.
    """
    strains = []

    # Define a regular expression pattern to match strain names
    strain_pattern = r"[A-Z]/\w+/.+/\d{4}"

    # Find the most likely column containing strain names
    most_likely_col_start = col_start

    strain_col_idx = None
    for col_idx in range(most_likely_col_start - 1, -1, -1):  # Iterate from col_start to the left
        strain_count = 0
        for row_idx in range(row_end):
            cell_value = str(worksheet.cell_value(row_idx, col_idx))
            if re.match(strain_pattern, cell_value):
                strain_count += 1
                strains.append(cell_value)
        if strain_count > 0:
            strain_col_idx = col_idx
            break
    return {
        "strain_col_idx": strain_col_idx,
        "strain_names": strains
    }

def find_antigen_rows(worksheet, row_start, col_start, col_end, strain_names=None):
    """
    Find the row containing cell passage data and the row containing abbreviated antigen names.
    """
    # Define a regular expression pattern to match cell passage data
    cell_passage_pattern = r"(MDCK\d+|SIAT\d+|E\d+)"

    # Find the row containing cell passage data
    cell_passage_row_idx = None
    for row_idx in range(row_start - 1, -1, -1):  # Iterate from row_start to the top
        cell_passage_count = 0
        for col_idx in range(worksheet.ncols):
            cell_value = str(worksheet.cell_value(row_idx, col_idx))
            if re.match(cell_passage_pattern, cell_value):
                cell_passage_count += 1
        if cell_passage_count > 0:
            cell_passage_row_idx = row_idx
            break
    
    # Define a regular expression pattern to match abbreviated antigen names
    abbrev_antigen_pattern = r"\w+/\d+.*"
    antigen_mapping = {}
    strain_idx = 0

    # Find the row containing abbreviated antigen names
    abbrev_antigen_row_idx = None

    for row_idx in range(cell_passage_row_idx + 1, worksheet.nrows):
        abbrev_antigen_count = 0
        for col_idx in range(col_start, col_end):
            cell_value = str(worksheet.cell_value(row_idx, col_idx))
            if re.match(abbrev_antigen_pattern, cell_value):
                abbrev_antigen_count += 1
                antigen_mapping[cell_value] = strain_names[strain_idx]
                strain_idx += 1
                
        if abbrev_antigen_count > 0:
            abbrev_antigen_row_idx = row_idx
            break

    return {
        "cell_passage_row_idx": cell_passage_row_idx,
        "abbrev_antigen_row_idx": abbrev_antigen_row_idx,
        "antigen_mapping": antigen_mapping
    }


def main():
    args = parse_args()

    # Load the Excel file
    workbook = xlrd.open_workbook(args.file)
    worksheet = workbook.sheet_by_index(0) # first sheet or loop

    # Find the block of titers in the worksheet
    titer_block = find_titer_block(worksheet)

    strain_block = find_strain_column(
        worksheet = worksheet,
        col_start = titer_block['col_start'][0][0],
        row_end = titer_block['row_end'][0][0]
    )
    antigen_block = find_antigen_rows(
        worksheet = worksheet,
        row_start=titer_block['row_start'][0][0],
        col_start=titer_block['col_start'][0][0],
        col_end=titer_block['col_end'][0][0],
        strain_names=strain_block['strain_names']
    )
    
    # Print the most likely row and column indices for the titer block
    print(f"Most likely (n={titer_block['col_start'][0][1]}) col_start: {titer_block['col_start'][0][0]}")
    print(f"Most likely (n={titer_block['col_end'][0][1]}) col_end: {titer_block['col_end'][0][0]}")
    print(f"Most likely (n={titer_block['row_start'][0][1]}) row_start: {titer_block['row_start'][0][0]}")
    print(f"Most likely (n={titer_block['row_end'][0][1]}) row_end: {titer_block['row_end'][0][0]}")

    # Print serum and virus annotations row and column indices
    print(f"Most likely strain column index: {strain_block['strain_col_idx']}")
    print(f"Most likely strain names: {strain_block['strain_names']}")
    print(f"Most likely cell passage row index: {antigen_block['cell_passage_row_idx']}")
    print(f"Most likely abbreviated antigen row index: {antigen_block['abbrev_antigen_row_idx']}")

    # Match abbreviated names across the top to the full names along the left side and auto convert to full names
    if antigen_block['abbrev_antigen_row_idx'] is not None:
        print("Antigen mapping:")
        for abbrev, full in antigen_block['antigen_mapping'].items():
            print(f"  {abbrev} -> {full}")
    

if __name__ == "__main__":
    main()
