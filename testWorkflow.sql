SELECT distinct SPROCESS.SERV_PROV_CODE, SPROCESS.R1_PROCESS_CODE, substring(SD_PRO_ID1,1,3) TaskID, SPROCESS.SD_PRO_DES,  R3STATYP.R3_ACT_STAT_DES, (CASE
    WHEN R3STATYP.R3_ACT_STAT_FLG = 'U'  THEN 'N/A'
    WHEN R3STATYP.R3_ACT_STAT_FLG = 'L'  THEN substring(SD_NXT_ID1,10,3)
    WHEN R3STATYP.R3_ACT_STAT_FLG = 'B'  THEN substring(SD_NXT_ID1,4,3)
    WHEN R3STATYP.R3_ACT_STAT_FLG = 'Y'  THEN substring(SD_NXT_ID1,1,3)
    END) Next, sprocess.asgn_agency_code + '/' + sprocess.asgn_bureau_code + '/' + sprocess.asgn_division_code as AssignedTo
    FROM SPROCESS INNER JOIN R3STATYP ON SPROCESS.R1_PROCESS_CODE = R3STATYP.R3_PROCESS_CODE and r3statyp.r3_act_type_des = SPROCESS.SD_PRO_DES
    WHERE SPROCESS.REC_STATUS='A' AND R3statyp.rec_status='A'
    order by r1_process_code, substring(sd_pro_id1,1,3)