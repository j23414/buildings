#! /usr/bin/env python3

"""Harmonize and merge pandas DataTables such that conflicting data is not lost.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  one_df = pd.DataFrame(
    {'strain': ['A', 'B', 'C'],
     'date': ['2022-01-01', '2022-02-02', '2022-03-03'],
     'clade': ['alpha', 'beta', 'gamma'],
    'geo':['iowa', 'washington', np.nan]})
  one_df['age'] = '-N/A-'

  two_df = pd.DataFrame(
    {'strain': ['D', 'B', 'C'],
     'clade': ['delta', 'beta2', 'gamma'],
    'patient': ['bob', 'marley', 'rick']})
  two_df['col_date'] = np.nan
  two_df['group'] = ''

  print(one_df)
  print(two_df)

  merged_df = merge_two(one_df, two_df)
  print(merged_df)
"""

# ===== Dependencies
import pandas as pd
import numpy as np

import sys
import argparse
import os

# (2) Define command line arguments
def parse_args():
    # Main help command
    parser = argparse.ArgumentParser(
        description = "USAGE: python uniq_merge.py --cache 'data/zika.tsv' --new 'data/ncbi.tsv'"
    )
    # Add first argument
    parser.add_argument(
        "--cache",
        help = "Path to cache of cleaned data.",
        required = True
    )
    parser.add_argument(
        "--new",
        help = "Path to new data.",
        required = True
    )
    
    return parser.parse_args()

# ===== Reusable functions
def _drop_uninformative_cols(df:pd.DataFrame) -> pd.DataFrame:
    """Drops uninformative columns from a pandas DataFrame for being all empty. Used by merge_two."""
    return(df.replace('', np.nan).replace('-N/A-', np.nan).dropna(how = 'all', axis = 1))

def _uniq_merge(x: 'pd.Series[str]') -> str:
    """Merges unique values by group and joins conflicting values in a comma separated list. Used by merge_two."""
    cx = x.replace('', np.nan).replace('-N/A-', np.nan).dropna().unique()
    if(len(cx) >= 1):
        return(','.join(cx))
    else:
        return('')

# Merge and harmonize two datasets, flag conflicts with commas
def merge_two(df1:pd.DataFrame, df2: pd.DataFrame, groupby_col: str = 'strain') -> pd.DataFrame:
    """Harmonizes and merges two pandas DataFrames.

    Takes two pandas DataFrames through the following 3 steps:

    1. Drops any columns in either which are all NA, "-N/A", or empty strings
    2. Harmonizes their columns such that columns in the left DataFrame are preferentially listed first
    3. Combines the DataFrames by group defined in groupby_col such that:
      * unique values are merged
      * conflicting values are joined in a comma separated list

    Args:
      df1:
        The left hand side (lhs) pandas DataTable, will preferentially decide column order of merged DataTable
      df2:
        The right hand side (rhs) pandas DataTable, will be merged with df1 and new columns will be listed later.
      groupby_col:
        The id column that is shared by both df1 and df2 to allow for merging and harmonization of datasets

    Returns:
      A merged and harmonized dataset of containing information from df1 and df2.

    Raises:
      TBD
    """
    # Drop uninformative columns
    df1 = _drop_uninformative_cols(df1)
    df2 = _drop_uninformative_cols(df2)
    
    # Harmonize columns
    new_col = [x for x in df2.columns.tolist() if x not in set(df1.columns.tolist())]
    h_df1_df = df1.reindex(df1.columns.tolist() + new_col, axis = 1)
    h_df2_df = df2.reindex(df1.columns.tolist() + new_col, axis = 1)
    
    # Unique and merge conflicting data
    merged_df = pd.concat([h_df1_df, h_df2_df]).groupby(groupby_col).agg([_uniq_merge])
    return(merged_df)


def main():
    args = parse_args()

    print(args)
    # ===== Test Data and Demo 
    print('one_df:')
    
    one_df = pd.DataFrame(
        {'strain': ['A', 'B', 'C'],
        'date': ['2022-01-01', '2022-02-02', '2022-03-03'],
        'clade': ['alpha', 'beta', 'gamma'],
        'geo':['iowa', 'washington', np.nan]})
    one_df['age'] = '-N/A-'
    print(one_df)
    
    print('two_df:')
    two_df = pd.DataFrame(
        {'strain': ['D', 'B', 'C'],
        'clade': ['delta', 'beta2', 'gamma'],
        'patient': ['bob', 'marley', 'rick']})
    two_df['col_date'] = np.nan
    two_df['group'] = ''
    print(two_df)
    
    print('merged_df:')
    
    x_df = merge_two(one_df, two_df)
    print(x_df)


if __name__ == '__main__':
    main()