LIBNAME DW_TEST SQLSERVER SERVER=PROD1 SCHEMA=s_schema user = &userid password = "&password";
data _null_;
proc sql; 
 create table t_table3 as select col1, col2, col3, col4 from t_schema.table2 join t_schema.table8 on table2.idx = table8.idx group by 1, 2, 3, 4; 
quit;
%INCLUDE "test_data/deeper_test_data/sas_script_d1.sas";data new; set old;
* This is a comment;
