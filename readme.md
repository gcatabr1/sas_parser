
<h1 align="center">
  <br>

  <br>
  SAS Parser
  <br>
</h1>

<h4 align="center">Text Parser to Normalized CSV in <a href="https://www.python.org" target="_blank">Python</a>.</h4>

<p align="center">
  <a href="https://img.shields.io/badge/maintained-yes-blue"></a>
    <img src="https://img.shields.io/badge/maintained-no-blue" alt="maintained - yes">
  </a>
  <a href="https://www.python.org/" title="Go to Python homepage"><img src="https://img.shields.io/badge/Python-1-blue?logo=python&logoColor=white" alt="Made with Python"></a>
</p>

<p align="center">
  <a href="#problem">Problem</a> •
  <a href="#approach">Approach</a> •
  <a href="#proposed-solution">Proposed Solution</a> •
  <a href="#requirements">Requirements</a> • 
  <a href="#how-to-run">How To Run</a> •
  <a href="#technical">Technical</a> •
  <a href="#notes">Notes</a> •
  <a href="#to-do">To-Do</a>
</p>

## Problem

Problem frame: No comprehensive inventory of SAS scripts; both inventory of files as well as inventory of contents.
For example, cannot answer questions like:

- How many SAS scripts are there across multiple directories, when were they created and last accessed?
- How can I find out which SAS scripts reference a specific data table?
- How can I find what SAS scripts reference / import other SAS scripts, and which ones?
- How can I find SAS scripts that reference a particular SQL table column?
- How can I find SAS scripts that have hardcoded dates?
- and so on...

</br>

## Approach

Attempting to predict all code content questions is an intractable problem. An approach to facilitate all manner of information needs
would be to create a generalized approach that allows a developer to create a ***parser*** that can generate queryable results to answer
specific questions.

One way this could be approached is by using specific commands already provided by the OS. For example, if you wanted to know the line count
for each SAS script in a directory, you might use the WC command. Or if you wanted to know which scripts contained hardcoded dates, you could
use the SED and regex. But this approach could get messy and the results would not be a uniform format for doing aggregate queries.

The approach used here is more generalized and consistent - one that can work on a range of OS's, requiring only knowledge of Python and SQL.

1. ***main routine*** that executes any number of predefined [Python] parser functions on a directory (and sub-directories). This ***main routine***
sequentially executes the list of parsers on each specified ***file type*** in the directory and then outputs the results to csv files in a directory,
also specified on the command line.

2. ***parser*** functions that mine information from one or more [text] scripts - returning it in a format (CSV) that can be ingested by most databases
and then queried for various aspects of that parsed information.


</br>

## Proposed Solution
![overview](/images/parser_overview.png)

The solution consists of 2 python scripts:

1. sas_parser2.py
2. parse_functions.py

where sas_parser2.py contains the main routine for

1. ingesting the cli parameters,
2. writing the list of parse functions that will be executed to the ***dim_func*** dataframe
3. reading the directory and creating the list of files to be inspected
4. writing the file list to the ***summary*** dataframe
5. executing the parse functions one at a time on each of the files
6. writing the results of each parse function to the ***detail*** dataframe
7. writing out each of the dataframes to their respective CSV files
</br>

## Requirements

Python 3.x
Python environment with the following packages installed:

- pandas
- tqdm

</br>

## How To Run

### Parsing

To run the code with pre-selected parsers, first clone the repository, activate the python environment and then perform any of the following:

```bash
# command and example command line arguments for sas files
# -i is the input directory, -t is the file extension, -o is the output directory
> python sas_python2.py -i 'some_directory_of_scripts' -t 'sas' -o 'results'
```

On execution, the python script will output a status bar as it performs each of the parsers on the file directory specified.

![command](/images/sas_parser_command.png)

> **Note**
> If you only want specific parsers to execute, you will need to edit the sas_parser2.py file and modify the variable ***functions_to_apply***

![functions_to_apply](/images/functions_to_apply.png)

### Querying

The easiest way to work with the sas_parser2.py output CSV files is to import them into a database and query for the
particular details you are interested in.

Assuming you have already imported the CSV files into a database you could do something like the following:

## Technical

TBD

## Notes

## To-Do

Things to consider adding or improving on:

- parallelizing (muliprocess package) the main parse routine
- pass a copy of the script (text) to each parser instead of the filename - so as to avoid opening the file for each parser
