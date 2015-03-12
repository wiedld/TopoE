import datetime
from urllib2 import Request, urlopen, URLError


# This file should include the api call to CAISO, cron every 10 minute.  Collects realtime data which updates every 10 minutes.


########################################################
## DATA SOURCE DOCUMENTATION:
# http://www.caiso.com/Documents/InterfaceSpecifications-OASIS_v4_2_4_Clean.pdf

## IMPORTANT NOTE:  singlezip and groupzip customized request are error prone due to changling syntax requirements in the get request.
        #  instead, use the bundled requests that contain the following

        # SLD_FCST
        #     SYS_FCST_ACT_MW       actual demand, hrly
        #     SYS_FCST_5MIN_MW      operating interval RTD forecast, 5 min
        # SLD_REN_FCST
        #     RENEW_FCST_DA_MW      forecast renewables for the day, hrly
        #     RENEW_FCST_ACT_MW     actual renewables, hrly
        #     RENEW_FCST_5MIN_MW    operating interval RTD forecast, 5 min

###################################################################

# SYS_FCST_5MIN_MW

    # http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=RTM&execution_type=RTD&startdatetime=20130919T07:00-0000&enddatetime=20130920T07:00-0000&version=1&as_region=ALL

    # <REPORT_DATA>
    # <DATA_ITEM>SYS_FCST_5MIN_MW</DATA_ITEM>
    # <RESOURCE_NAME>CA ISO-TAC</RESOURCE_NAME>
    # <OPR_DATE>2013-09-19</OPR_DATE>
    # <INTERVAL_NUM>98</INTERVAL_NUM>
    # <INTERVAL_START_GMT>2013-09-19T15:05:00-00:00</INTERVAL_START_GMT>
    # <INTERVAL_END_GMT>2013-09-19T15:10:00-00:00</INTERVAL_END_GMT>
    # <VALUE>26255</VALUE>
    # </REPORT_DATA>

####################################################################

# SYS_FCST_ACT_MW

    # http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=ACTUAL&startdatetime=20130919T07:00-0000&enddatetime=20130920T07:00-0000&version=1&as_region=ALL

    # <REPORT_DATA>
    # <DATA_ITEM>SYS_FCST_ACT_MW</DATA_ITEM>
    # <RESOURCE_NAME>CA ISO-TAC</RESOURCE_NAME>
    # <OPR_DATE>2013-09-19</OPR_DATE>
    # <INTERVAL_NUM>18</INTERVAL_NUM>
    # <INTERVAL_START_GMT>2013-09-20T00:00:00-00:00</INTERVAL_START_GMT>
    # <INTERVAL_END_GMT>2013-09-20T01:00:00-00:00</INTERVAL_END_GMT>
    # <VALUE>33493</VALUE>
    # </REPORT_DATA>


####################################################################

## TODO:  possibily in future?  The above xml files are not seeming to download per different regions.  failed with "as_region=" "as_region_id=" "tac_zone_name=" "tac_area_name="
    # also tried "pnode_name=" using the few pnodes.  failed.
    # complete list of pnodes are here:
    # http://oasis.caiso.com/oasisapi/SingleZip?queryname=ATL_TAC_AREA_MAP&startdatetime=20130919T07:00-0000&enddatetime=20130920T07:00-0000&version=1


# <TAC_AREA_NAME>TAC_NORTH</TAC_AREA_NAME>
#     <PNODE_NAME>NARROWS2_7_B1</PNODE_NAME>
#     <PNODE_NAME>HMBUNIT1_7_GN010</PNODE_NAME>
#     <PNODE_NAME>ALMDACT1_7_B1</PNODE_NAME>
#     <PNODE_NAME>BONNIEN_7_N002</PNODE_NAME>
#     <PNODE_NAME>COLGATE1_7_B1</PNODE_NAME>
#     <PNODE_NAME>HURONGEN_7_ND002</PNODE_NAME>
#     <PNODE_NAME>PTS7SWNG_7_B2</PNODE_NAME>
#     <PNODE_NAME>DINUBAE_7_B2</PNODE_NAME>
#     <PNODE_NAME>CYMRIC_1_N004</PNODE_NAME>

# <TAC_AREA_NAME>TAC_ECNTR</TAC_AREA_NAME>
#     <PNODE_NAME>REDON6G_7_B1</PNODE_NAME>
#     <PNODE_NAME>HUNT3G_7_B1</PNODE_NAME>
#     <PNODE_NAME>VESTAL_6_GN010</PNODE_NAME>
#     <PNODE_NAME>ETIWANDA_6_N004</PNODE_NAME>
#     <PNODE_NAME>SERRFGEN_7_B1</PNODE_NAME>
#     <PNODE_NAME>VILLAPK_6_GN002</PNODE_NAME>

# <TAC_AREA_NAME>TAC_SOUTH</TAC_AREA_NAME>
#     <PNODE_NAME>MESARIM_6_GN001</PNODE_NAME>


####################################################################


def main():
    current = datetime.datetime.now()
    current_str = str(current)

    try:
        response = urlopen("http://oasis.caiso.com/oasisapi/SingleZip?queryname=SYS_FCST_5MIN_MW&startdate=20150301T00:00-0000&enddate=20150302T00:00-0000&market_run_id=DAM&version=v1&as_type=ALL&as_region=ALL")
        caiso_rt = response.read()
        print ("api response:", caiso_rt)

         ## TODO: check values within expected bounds, confirm timestamp is new, and update into db of dynamic data

    except URLError:
        print ("Error.  CAISO_api failure at",current_str)

        f = open('log_file.txt','a')
        f.write("\nError.  CAISO_api failure at: " +current_str)
        f.close



if __name__ == "__main__":
    main()