"""
SAS PARSER
file: sas_parser.py
author: g.cattabriga
date: 2023.05.27
      2023.06.06
        update to use dataframes and 3 tables
version: 2.0
purpose: python script (main function) to execute one or more parse functions on one or more sas (text) files in a specified directory
        this creates 2 files, a summary_yymmddhhmmss.csv file and a summary_yymmddhhmmss.csv file
        the summary file contains the list of file names, directories and date attributes (create, modified) evaluated
        the detail file contains the results of each parse function performed on each file in the summary
example use: python sas_parser.py -i 'test_data' -t 'sas' -o 'results'
        where 'test_data' is the directory of text data to be parsed, 'sas' is the file type (.sas.) and
        'results' is the directory the summary and details will be saved.

notes: the parsing / evaluation functions are in the parse_functions.py file 
todo: 
        creating a third table, where the first table remains the header, the second table is the cross table to 
        the header table and to the detail table so as to accommodate multiple values for a single metric
        use dataframes to create primary keys

        function that returns key elements of a SQL statement (e.g. table names, column names)

        If performance becomes and issue, then don't keep opening the file, but instead pass the contents 
        of the file to the parse functions. 
"""


import argparse
import os
import inspect
import pandas as pd
from tqdm import tqdm
import datetime
from parse_functions import *   # import all the parse functions 


# This function is designed to recursively scan through the specified directory, finding all files of the specified type
def get_file_list(directory, file_type):
    return [os.path.join(root, file) for root, dirs, files in os.walk(directory) for file in files if file.endswith(file_type)]


# List of functions to apply
functions_to_apply = [
    get_file_info,
    count_lines, 
    count_sql, 
    get_sql_code, 
    get_libname_lines, 
    count_exports, 
    count_null_ds, 
    find_date_lines,
    find_file_references] 

def main(input_dir, output_dir, file_type):
    file_list = get_file_list(input_dir, file_type)

    summary_df = pd.DataFrame(columns=['summ_idx', 'f_name', 'dir_path', 'create_dt', 'modified_dt'])
    xref_df = pd.DataFrame(columns=['summ_idx', 'xref_idx', 'func_descr'])
    detail_df = pd.DataFrame(columns=['xref_idx', 'func_value'])

    summary_index = 1
    xref_index = 1

    for file_path in tqdm(file_list, desc="Processing files"):
        dir_name, file_name = os.path.split(file_path)  # get directory and filename
        file_info_name, file_info_values = get_file_info(file_path)

        for file_info in file_info_values:
            file_info.update({'summ_idx': summary_index, 'f_name': file_name, 'dir_path': dir_name})
            summary_df = summary_df.append(file_info, ignore_index=True)

        for func in functions_to_apply:
            num_args = len(inspect.signature(func).parameters)
            if num_args == 1:
                result_name, vals = func(file_path)
            elif num_args == 2:
                result_name, vals = func(file_path, file_list)
            for val in vals:
                xref_df = xref_df.append({'summ_idx': summary_index, 'xref_idx': xref_index,
                                          'func_descr': result_name}, ignore_index=True)
                detail_df = detail_df.append({'xref_idx': xref_index, 'func_value': val}, ignore_index=True)

                xref_index += 1

        summary_index += 1

    # These lines output the dataframes to CSV files, adding a timestamp to each filename
    dt_string = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    summary_df.to_csv(os.path.join(output_dir, 'summary_'+dt_string+'.csv'), index=False)
    xref_df.to_csv(os.path.join(output_dir, 'xref_'+dt_string+'.csv'), index=False)
    detail_df.to_csv(os.path.join(output_dir, 'detail_'+dt_string+'.csv'), index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('-i', '--input_dir', required=True, help='The input directory for files to be processed')
    parser.add_argument('-o', '--output_dir', required=True, help='The output directory for processed files')
    parser.add_argument('-t', '--file_type', required=True, help='The file type to be processed')
    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.file_type)


