run;
proc means data=sashelp.class; run;
PROC DATASETS LIBRARY=mylib;
CONTENTS DATA=mytable;
QUIT;
data _null_;
filename myfile "/path/to/file";
LIBNAME DW_TEST SQLSERVER SERVER=PROD1 SCHEMA=s_schema user = &userid password = "&password";
LIBNAME DW_TEST SQLSERVER SERVER=PROD1 SCHEMA=s_schema user = &userid password = "&password";
