data _null_;
proc means data=sashelp.class; run;
%INCLUDE "test_data/deeper_test_data/sas_script_d1.sas";data new; set old;
proc print data=sashelp.class; run;
proc print data=sashelp.class; run;
PROC DATASETS LIBRARY=mylib;
CONTENTS DATA=mytable;
QUIT;
