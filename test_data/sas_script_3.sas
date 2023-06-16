%let password = something

* Create a library for our datasets;
LIBNAME mylib 'c:\myfolder';

* Use PROC SQL with stimer option to track performance;
options fullstimer;
PROC SQL STIMER;
    CREATE TABLE mylib.mytable AS 
    SELECT * 
    FROM sashelp.class;
QUIT;

* Define a macro to summarize a variable;
%macro summarize_data(lib, data, var);
    PROC MEANS DATA=&lib..&data;
        VAR &var;
    RUN;
%mend summarize_data;

* Use our macro to summarize Weight in mytable;
%summarize_data(mylib, mytable, Weight);

* Use a data step to print names to the log;
DATA _NULL_;
    SET mylib.mytable;
    FILE PRINT;
    PUT 'The name is ' Name;
RUN;

* Export our dataset to a CSV file;
PROC EXPORT DATA=mylib.mytable
    OUTFILE='C:\myfolder\mytable.csv'
    DBMS=CSV
    REPLACE;
RUN;
