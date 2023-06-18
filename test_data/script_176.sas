%INCLUDE "test_data/deeper_test_data/sas_script_d1.sas";data new; set old;
%let password = password_exposed;
proc means data=sashelp.class; run;
LIBNAME DW_TEST SQLSERVER SERVER=PROD1 SCHEMA=s_schema user = &userid password = "&password";
proc print data=sashelp.class; run;
proc print data=sashelp.class; run;
LIBNAME DW_TEST SQLSERVER SERVER=PROD1 SCHEMA=s_schema user = &userid password = "&password";
