<!-- control total directory -->
<!--
Author: Gary Cattabriga
Date: 2023.05.28
*** markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- WORKSPACE LOGO -->
<br />
<p align="center">
  <h1 align="center">SAS Parser</h1>
  <p align="center">
  <br />
  </p>
</p>

### Version
**0.1.0**

 <br/>
## Overview
The **parse_functions.py** module contains functions for parsing / evaluating SAS scripts and returning associated values. For each function, the file evaluated, the metric name and associated values (sometimes more than one value are returned as a string list) are returned. There may be an occasion where more than the file path is passed in. The **sas_parser.py** is the main module that reads the input directory and returns the corresponding files. These files are output as the summary_yyyymmddhhmmss.csv file. This main module will then execute the named parse functions outputting the values into the detail_yyyymmddhhmmss.csv file.


<br/>
### Getting Started
##### Required 

```

```
<br/>


```

```

<br/><br/>
## Example Usage

Parse the ***.sas*** files in the ***test_data*** directory and output the results to the ***results*** directory
```
> python sas_parser.py -i 'test_data' -t 'sas' -o 'results' 
```



<br/>



<br/>





<br/><br/>


<br/><br/>

## Technical Code Description
 
