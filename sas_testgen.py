import argparse
import os
import random
from tqdm import tqdm

# Possible lines to add in SAS script
sas_code_list = [
    '* This is a comment;',
    'data _null_;',
    'run;',
    'proc sql; \r\n select col1, col2, col3 from t_schema.table1 where co1 = "some_string"; \r\nquit;',
    'proc sql; \r\n create table t_table3 as select col1, col2, col3, col4 from t_schema.table2 join t_schema.table8 on table2.idx = table8.idx group by 1, 2, 3, 4; \r\nquit;',
    'LIBNAME DW_TEST SQLSERVER SERVER=PROD1 SCHEMA=s_schema user = &userid password = "&password";',
    '%INCLUDE "test_data/deeper_test_data/sas_script_d1.sas";'
    'data new; set old;',
    'proc print data=sashelp.class; run;',
    'filename myfile "/path/to/file";',
    'DATA _NULL_;\r\nSET mylib.mytable;\r\nFILE "c:\myfolder\log.txt";\r\nPUT "The name is " Name;\r\nRUN;',
    'data _null_; set sashelp.class; file myfile; put (_all_)(=); run;',
    'proc means data=sashelp.class; run;',
    'PROC DATASETS LIBRARY=mylib;\r\nCONTENTS DATA=mytable;\r\nQUIT;',
    '%macro summarize_data(lib, data, var);\r\nPROC MEANS DATA=&lib..&data;\r\nVAR &var;\r\nRUN;\r\n%mend summarize_data;',
    '%let password = password_exposed;'
]

def generate_sas_scripts(num_scripts, min_lines, max_lines, output_dir):
    """
    This function generates a specified number of SAS scripts with a random number of lines within a given range.
    
    Parameters:
    num_scripts (int): The number of SAS scripts to generate.
    min_lines (int): The minimum number of lines in a script.
    max_lines (int): The maximum number of lines in a script.
    output_dir (str): The directory where the generated SAS scripts will be saved.
    """
    # Iterate over the range of number of scripts to be created
    for i in tqdm(range(num_scripts), desc="Generating SAS scripts"):
        # Define the name of the script
        script_name = f"script_{i+1}.sas"
        # Create the full path of the script
        script_path = os.path.join(output_dir, script_name)
        
        # Randomly decide the number of lines within the given range
        num_lines = random.randint(min_lines, max_lines)

        # Open the file in write mode
        with open(script_path, 'w') as f:
            # For each line to be added
            for _ in range(num_lines):
                # Randomly select a line from the possible lines
                line = random.choice(sas_code_list)
                # Write the line to the file
                f.write(line + '\n')
        
        ## print(f"SAS script generated: {script_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random SAS scripts.")
    parser.add_argument("-n", "--num_scripts", type=int, help="Number of scripts to generate.")
    parser.add_argument("-min", "--min_lines", type=int, help="Minimum number of lines in a script.")
    parser.add_argument("-max", "--max_lines", type=int, help="Maximum number of lines in a script.")
    parser.add_argument("-o", "--output_dir", help="Output directory for SAS scripts.")
    args = parser.parse_args()

    generate_sas_scripts(args.num_scripts, args.min_lines, args.max_lines, args.output_dir)
