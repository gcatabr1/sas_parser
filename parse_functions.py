import re
import datetime
import os

#-----------------------------------------------------------------------------
# This function is designed to extract basic information about the file, such as its creation and modification dates
def get_file_info(file_path):
    return 'file_info', [{'create_dt': datetime.datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
                          'modified_dt': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),}]
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Define function to count the number of lines in a file
def count_lines(file_path):
    """Count the number of lines in a file

    Args:
        file_path (string): full path to the file

    Returns:
        integer: the number of lines in the file
    """
    with open(file_path, 'r', encoding='cp1252') as file:  # Open the file
        lines = file.readlines()  # Read all lines into a list
    return ("line_count", [len(lines)])  # Return the number of lines
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Define function to count the number of 'proc sql / quit;' pairs
def count_sql(file_path):
    """Count the number of SQL statements

    Args:
        file_path (string): full path to the file

    Returns:
        integer: count of the number of SQL statements
    """
    with open(file_path, 'r', encoding='cp1252') as file:  # Open the file
        content = file.read()  # Read the entire file into a string
    return ("sql_count", [len(re.findall("proc sql.*?quit;", content, flags=re.IGNORECASE | re.DOTALL))])
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Define function to find SQL blocks
def get_sql_code(file_path):
    """This function parses a text file looking for SQL blocks (defined by proc sql / quit; pair) and returns the line number and corresponding SQL code

    Args:
        file_path (string): full file path to be parsed

    Returns:
        tuple of form (int, string): returns line number and sql code block pair
    """
    sql_blocks = []
    with open(file_path, 'r', encoding='cp1252') as file:
        lines = [line.strip() for line in file.readlines()]
    # We initialize block and start_line to None as we haven't found a block yet
    block = None
    start_line = None
    for i, line in enumerate(lines):
        if 'proc sql' in line.lower():
            # If we find 'proc sql', we start a new block
            block = []
            start_line = i + 1  # Line numbers start at 1
        elif block is not None:
            # If we're inside a block, we add the line to the block
            if 'quit;' in line.lower():
                # If we find 'quit;', we end the block and add it to sql_blocks
                sql_blocks.append((start_line, ' '.join(block))) # Join lines into one string
                block = None  # Reset block for the next one
            else:
                block.append(line)
    return ("sql_code", sql_blocks)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Define function to find lines starting with 'LIBNAME'
def get_libname_lines(file_path):
    """Return any line in the file with a LIBNAME function

    Args:
        file_path (string): full file path to be parsed

    Returns:
        string: list of the lines having a LIBNAME function
    """
    libname_lines = []
    with open(file_path, 'r', encoding='cp1252') as file:  # Open the file
        lines = file.readlines()  # Read all lines into a list
    for line in lines:  # For each line
        if line.lower().startswith('libname'):  # If it starts with 'libname' (case insensitive)
            libname_lines.append(line)  # Add it to the list
    return ("libname", libname_lines)  # Return the list of matching lines
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Define function to find lines containing 'password'
def get_password_lines(file_path):
    """Return any line in the file with a reference to 'password'

    Args:
        file_path (string): full file path to be parsed

    Returns:
        string: list of the lines containing the string 'password'
    """
    password_lines = []
    with open(file_path, 'r', encoding='cp1252') as file:  # Open the file
        lines = file.readlines()  # Read all lines into a list
    for line in lines:  # For each line
        if line.lower().find('password') != -1:  # If it contains 'password' (case insensitive)
            password_lines.append(line)  # Add it to the list
    return ("password", password_lines)  # Return the list of matching lines
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# Define function to count the number of 'proc export / run;' pairs
def count_exports(file_path):
    """Return the number of 'proc export / run;' pairs

    Args:
        file_path (string): full file path to be parsed

    Returns:
        integer: count of proc export blocks
    """
    with open(file_path, 'r', encoding='cp1252') as file:  # Open the file
        content = file.read()  # Read the entire file into a string
    return ("export_count", [len(re.findall("proc export.*?run;", content, flags=re.IGNORECASE | re.DOTALL))])
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Define function to count the number of '_null_ / run;' pairs
def count_null_ds(file_path):
    """Return the number of of _null_ dataset blocks in the given file

    Args:
        file_path (string): full file path to be parsed

    Returns:
        integer: count of _null_ dataset blocks
    """
    with open(file_path, 'r', encoding='cp1252') as file:  # Open the file
        content = file.read()  # Read the entire file into a string
    return ("null_ds_count", [len(re.findall("_null_.*?run;", content, flags=re.IGNORECASE | re.DOTALL))])
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Define function to find lines with hardcoded dates
def find_date_lines(file_path):
    """Find lines containing strings that 'look like' hardcoded dates of format yyyy-mm-dd

    Args:
        file_path (string): full file path to be parsed

    Returns:
        tuple of form (int, string): returns line number and date string pair
    """
    date_lines = []
    with open(file_path, 'r', encoding='cp1252') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        # Find any date in the format yyyy-mm-dd
        matches = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', line)
        if matches:
            # If a date is found, add the line number (i+1) and the dates to the list
            date_lines.append((i+1, matches))
    return ("hardcoded_dates", date_lines)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Define function to find references to other files
def find_file_references(file_path, file_list):
    """Find lines containing a file reference - from the file_list, which is a list of all files evaluated

    Args:
        file_path (string): full file path to be parsed
        file_list ([string]): list of strings representing all of the files to be checked against

    Returns:
        tuple of form (int, string): returns line number and date (yyyy-mm-dd) found in the file_path
    """
    file_references = []
    file_list = [sub.replace('\\', '/') for sub in file_list]   # fix path issue with windows
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    for i, line in enumerate(lines):
        for referenced_file in file_list:
            # If the line contains the filename, add it to the list of references
            if referenced_file in line:
                file_references.append((i + 1, referenced_file))
    return ("file_ref", file_references)
#-----------------------------------------------------------------------------