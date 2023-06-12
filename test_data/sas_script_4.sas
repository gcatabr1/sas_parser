%let sasu = %sysfunc(pathname(sasuser));
%include "Ifin_ops/medenc/password/password.sas";
LIBNAME DWU_EDW TERADATA SERVER=PRDEDW2 SCHEMA=DWU_EDW_RB DEFER=YES user = &userid password = "&password";
LIBNAME DWU_PRC TERADATA SERVER=PRDEDW2 SCHEMA=DWU_PRC_RB DEFER=YES user = &userid password = "&password";
libname common '/fin_ops/medenc/common';
LIBNAME mytera TERADATA SERVER=PRDEDW2 user = &userid password = "&password" database=sb_mc_enctr;
options validvarname=any;
proc Datasets lib=work kill memtype=data;
run;
%let to_Email = "";
%let cc_email = "samuel.Bevilacqua@cvshealth.com";
%let family = 'CarelonRx - Elevance TX';
data _null_;
call symput Cfamx','FSR'11%sysfunc(Translate(&family,"_"," ")));
call symput ('fam2',&family);
call symput Cfam3',%sysfunc(compress(&family)));
run;
%put &famx;
%put &fam2;
%put &fam3;
%let datetime_start = %sysfunc(TIME());
%LET START_TIME = : %sysfunc(datetime(),datetime14.);
%put START TIME: %sysfunc(datetime(),datetime14.);
PROC SQL STIMER;
Select quote(trim(email)) into :To_Email SEPARATED BY " " from COMMON.DISTLISTS
WHERE Report = 'FSR_Antnem_TX' AND
Status = 'TO'
QUIT;
PROC SQL STIMER;
Select quote(trim(email)) into :CC_Email SEPARATED BY " " from COMMON.DISTLISTS
WHERE Report = 'FSR_Anthem_TX' AND
Status = 'CC'
QUIT;
%put &to_email;
%put &cc email;
proc sql;
select "'"Irtrim(clientid)II"'" into :cProfiles separated by "," from common.profl where family = &family;
quit;
%put ficprofiles;
%let xsstartems = 01Jan1960;
%macro setStartDate(intnxToday);
%if %substr(&intnxToday,3,3) = SEP I
%substr(&intnxToday,3,3) = OCT I
%substr(&intnxToday,3,3) = NOV I
%substr(&intnxToday,3,3) = DEC %then
%let xsstart_ems = 01Sep%sysfunc(substr(%sysfunc(intnx(year,%sysfunc(today()),-3,b),date9.),6,4),4.);
%else %let xsztart_ems = 01Sep%sysfunc(substr(%sysfunc(intnx(year,%sysfunc(today()),-4,b),date9.),6,4),4.);
%mend setStartDate;
%let startDate = %sysfunc(intnx(month,%sysfunc(today()),0,e),date9.);
%setStartDate(&startDate.)
%put &xsstart_ems;

%setStartDate(&startDate.)
%put &xsstart ems;
/*%let xeend = 31Aug2020;*/
%let xeend ems = 01Jan1960;
%macro setEndDate(intnxToday);
%if %substr(&intnxToday,3,3) =
%substr(&intnxToday,3,3) OCT I
%substr(&intnxToday,3,3) = NOV I
%substr(&intnxToday,3,3) = DEC %then
%let xeend ems = 31Aug%sysfunc(substr(%sysfunc(intnx(year,%sysfunc(today()),1,b),date9.),6,4),4.);
%else %let xeend ems = 31Aug%sysfunc(substr(%sysfunc(intnx(year,%sysfunc(today()),0,b),date9.),6,4),4.);
%mend setEndDate;
%let endDate = %sysfunc(intnx(month,%sysfunc(today()),0,e),date9.);
%setEndDate(&endDate.)
%put &xeend;
%let startdatetime = %sysfunc(dhms("&xsstart_ems"d,0,0,0),datetime.);
%let enddatetime = %sysfunc(dhms("&xeend_ems"d,23,59,59),datetime.);
%let xsstart = %unquote(%str(95')%sysfunc(inputn(&xsstart_ems,date9.),yymmdd10.)%str(%'));
%let xeend = 95unquote(%str(ir')%sysfunc(inputn(&xeend_ems,date9.),yymmdd10.)%str(V));
put &xsstart &xsstart ems &xeend &xeend ems &startdatetime &enddatetime;
/* Set date 2nd time to get the EDw format*/
*%let xsstart = '2018-09-01';
*%let xeend = '2020-08-31';
proc import out=work.anthem_cag_structure
datafile='/fin_ops/medenc/sassandbox/scripts/FSR/Anthem_CAG_Structure.xlsx'
dbms=x1sx;
run;
proc datasets nolist lib=mytera;
delete anthem cag structure;
quit;
proc Sql stimer noprint;
select distinct cats("'",1v11 - acct_gid,"'") into :pgid separated by ',' from dwu _ edw.v _ ems _ trnmt _ dtl as ect
where ect.clnt_profl_id in (&cProfiles);
select distinct cats("'",1v13_acct_gid,"'") into :pgid _3_ separated by ',' from dwu edw.v ems trnmt dtl as ect
where ect.clnt_profl_id in (&cProfiles);
quit;
%put &pgid &pgid_3;

put &pgid &pgid 3;



proc Sql;
CONNECT TO teradata (database=dwu_edw tdpid=prdedwl user=6.userid password="&password" connection=global);
CREATE TABLE work.ECA AS
SELECT * FROM CONNECTION TO TERADATA
/* Encountered*/
Select ECA.LVLl_acctid AS Carrier
, ECA.LVL2_acct_id AS acct
/* , coalesce(cag.FSR_DESC,'Unknown') as family*/
'• ENCOUNTERED' AS Ql Status
/* , eca.clmnbr*7
/* , eca.clm_seq_nbr*/
, eca.clm_txn_cd
, extract(year from ECA.srvc_dt) as yr
, extract(month from ECA.srvc_dt) As mth
, SUM(RBL_DUE_AMT) AS dollars
,substr(ect.OUTBD_STRNG_TXT,45,2) AS FAC_Submitted
,eca.LVLl_ACCT_ID
,eca.LVL2_ACCT_ID
,eca.LVL3 ACCT ID
FROM DWU_EDW.V_PHMCY CLMEMS_DTL AS ECA
inner join DWU_El3W.VMS_TRNMT_DTL AS ECT
ON ECA.PRMCY_CLM_kMS_DTL_GID EQ ECT.PHMCY_CLm_EMs_DTL_GID
AND ECA.clnt_profl_id in (&cProfiles)
AND ECT.clnt_profl_id in (&cProfiles)
AND cast(eca.clm_adjn_bgn_ts as date)BETWEEN &xsstart and &xeend
AND eca.srvc_dt BETWEEN &xsstartand&xeend
AND ect.srvc_dt BETWEEN &xsstartand&xeend
AND ECA.selfcrteb2_IND ne 'Y'
AND ECA.clm_txn_cd IN ('Bl', 'B2')
AND ECA.src_rec_stus_cd in ('A')
and eca.clm_typ_cd ne 'R'
and ect.src_hist_curr_cd eq 'C'
and ect.1v13_acct_gid IN (&pgid_3)
and ect.lvll_acct_gid IN (&pgid)
and eca.1v13_acct_gid IN (&pgid_3)
and eca.lvll_acct_gid IN (&pgid)
GROUP BY 1,2,3,4,5,6,8,9,10,11
ORDER BY 1,2,3,4,5,6,8,9,10,11
DISCONNECT FROM Teradata;
quit;


proc sql;
create table work.eca as
select
eca.Carrier
,eca.acct
,coalesce(cag.FSR_DESC,'Unknown') as family
,eca.Ql_Status
,eca.clm_txn_cd
,eca.yr
,eca.mth
,sum(eca.dollars) as dollars
,eca.FAC_Submitted
from work.eca
left join work.anthem_cag_structure as cag
on eca.LVLl_ACCT_ID = cag.carrier
and eca.LVL2_ACCT_ID = cag.acct
and eca.LVL3_acct_id = cag.grp
group by 1,2,3,4,5,6,7,9
order by 1,2,3,4,5,6,7,9;
quit;