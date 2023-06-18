proc means data=sashelp.class; run;
proc sql; 
 select col1, col2, col3 from t_schema.table1 where co1 = "some_string"; 
quit;
data _null_; set sashelp.class; file myfile; put (_all_)(=); run;
%INCLUDE "test_data/deeper_test_data/sas_script_d1.sas";data new; set old;
proc sql; 
 select col1, col2, col3 from t_schema.table1 where co1 = "some_string"; 
quit;
