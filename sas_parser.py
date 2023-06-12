"""
SAS PARSER
file: sas_parser.py
author: g.cattabriga
date: 2023.05.27
purpose: python script (main function) to execute one or more parse functions on one or more sas (text) files in a specified directory
notes: the parsing / evaluation functions are in the parse_functions.py file 
todo: 
        creating a third table, where the first table remains the header, the second table is the cross table to 
        the header table and to the detail table so as to accommodate multiple values for a single metric

"""

import os
import re
import argparse
import datetime
import csv
import inspect
from tqdm import tqdm
from parse_functions import *   # import all the parse functions 


def process_files(input_dir, output_dir, file_type):
    # List to store results of functions
    results = []

    # Get the current date and time to append to the output file names
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # File names for the output files
    summary_file_name = os.path.join(output_dir, f"summary_{now}.csv")
    detail_file_name = os.path.join(output_dir, f"detail_{now}.csv")

    # Find all files of the specified type in the input directory
    files_to_process = [os.path.join(dirpath, file)
                        for dirpath, dirnames, files in os.walk(input_dir)
                        for file in files if file.endswith(f".{file_type}")]


    # Write the file summary
    with open(summary_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["f_name", "dir_path", "create_dt", "modified_dt"])
        for file_path in files_to_process:
            writer.writerow([os.path.basename(file_path), os.path.dirname(file_path),
                            datetime.datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
                            datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()])

    # Run the functions on each file
    for file_path in tqdm(files_to_process, desc="Processing files", unit="file"):
        for func in functions_to_apply:
            num_args = len(inspect.signature(func).parameters)
            if num_args == 1:
                result_name, result_value = func(file_path)
            elif num_args == 2:
                result_name, result_value = func(file_path, files_to_process)
            results.append([os.path.basename(file_path), os.path.dirname(file_path), result_name, result_value])

    # Write the detailed results
    with open(detail_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["f_name", "dir_path", "func_descr", "func_value"])
        for result in results:
            writer.writerow(result)

#================================================================
# This is the entry point of the script
if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('-i', '--input_dir', type=str, required=True, help='Input directory')
    parser.add_argument('-t', '--file_type', type=str, required=True, help='File type to be processed')
    parser.add_argument('-o', '--output_dir', type=str, required=True, help='Output directory')

    
    # Parse command line arguments
    args = parser.parse_args()
    
    functions_to_apply = [
        count_lines, 
        count_sql, 
        get_sql_code, 
        get_libname_lines, 
        count_exports, 
        count_null_ds, 
        find_date_lines,
        find_file_references]  
    
    # Call the main function with the parsed arguments
    process_files(args.input_dir, args.output_dir, args.file_type)
