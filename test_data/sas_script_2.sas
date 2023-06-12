* Create a library for our datasets;
LIBNAME mylib 'c:\myfolder';

* Define a macro to summarize a variable;
%macro summarize_data(lib, data, var);
    PROC MEANS DATA=&lib..&data;
        VAR &var;
    RUN;
%mend summarize_data;

* Use our macro to summarize Height in mytable;
%summarize_data(mylib, mytable, Height);

* Use a data step to create a log;
DATA _NULL_;
    SET mylib.mytable;
    FILE 'c:\myfolder\log.txt';
    PUT 'The name is ' Name;
RUN;

* View the details of our dataset;
PROC DATASETS LIBRARY=mylib;
    CONTENTS DATA=mytable;
QUIT;
