import datetime
from urllib2 import Request, urlopen, URLError


# This file should include the api call to CAISO, cron every 10 minute.  Collects realtime data which updates every 10 minutes.



## DATA SOURCE DOCUMENTATION:
# http://www.caiso.com/Documents/SystemAccessInformation_MarketParticipants.pdf


# returned zip file naming convention:
#     startdate_enddate_Report Name_MktRunID_Stamp#.Zip
# within zip, file names:
#     startdate_enddate_Report Name_MktRunID_Stamp#.CSV

# codes to use as queryname:
#    XML Name:          XML Data Items:       Description:
#    PRC_FUEL           FUEL_PRC              Daily gas price
#    SLD_FCST_PEAK      SYS_PEAK_MW           hrly forecast for day
#    SLD_FCST           SYS_FCST_DA_MW        hrly DAM forecast
#                       SYS_FCST_2DA_MW       hrly DAM forecast, posted 2 days before
#                       SYS_FCST_ACT_MW       actual demand, hrly
#                       SYS_FCST_5MIN_MW      operating interval RTD forecast




def main():
    current = datetime.datetime.now()
    current_str = str(current)

    try:
        response = urlopen("http://oasis.caiso.com/oasisapi/SingleZip?queryname=SYS_FCST_ACT_MW&startdate=20150210&enddate=20150211&market_run_id=DAM&as_type=ALL&as_region=ALL")
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