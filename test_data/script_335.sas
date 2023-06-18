PROC DATASETS LIBRARY=mylib;
CONTENTS DATA=mytable;
QUIT;
LIBNAME DW_TEST SQLSERVER SERVER=PROD1 SCHEMA=s_schema user = &userid password = "&password";
filename myfile "/path/to/file";
PROC DATASETS LIBRARY=mylib;
CONTENTS DATA=mytable;
QUIT;
* This is a comment;
