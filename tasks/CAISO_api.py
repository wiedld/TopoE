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
# TODO:        #as_region=

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

    # http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=RTM&execution_type=RTD&startdatetime=20130919T07:00-0000&enddatetime=20130920T07:00-0000&version=1&as_region=ALL



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