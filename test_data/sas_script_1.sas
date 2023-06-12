* Connect to an Oracle database;
%INCLUDE "test_data/sas_script_2.sas";

PROC SQL;
    CONNECT TO ORACLE (USER=your_username PASSWORD=your_password PATH=your_path);
QUIT;

* Create a library for our datasets;
LIBNAME mylib 'c:\myfolder';

* Import a dataset from Oracle to our library;
PROC SQL;
    CREATE TABLE mylib.mytable AS 
    SELECT * 
    FROM connection to ORACLE
    (SELECT * FROM my_oracle_table);
QUIT;

* Export our dataset to a CSV file;
PROC EXPORT DATA=mylib.mytable
    OUTFILE='C:\myfolder\mytable.csv'
    DBMS=CSV
    REPLACE;
RUN;
