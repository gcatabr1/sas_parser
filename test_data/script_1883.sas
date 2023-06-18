data _null_; set sashelp.class; file myfile; put (_all_)(=); run;
data _null_;
proc print data=sashelp.class; run;
LIBNAME DW_TEST SQLSERVER SERVER=PROD1 SCHEMA=s_schema user = &userid password = "&password";
* This is a comment;
