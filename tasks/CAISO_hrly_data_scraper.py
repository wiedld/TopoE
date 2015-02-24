import datetime
import urllib2
from HB_project import model    # "relative" import.  create __init__ in parent dir.


"""This file is used to update the database table: HistoricCAISOProdByFuels.

    There are two basic tasks this file contains:
    (1) inital seeding of the db using many dates (hourly data for each date).
    (2) a recurring task each day.  To update the latest hourly data.

    There is also a web scaper function, get_historic_mw_by_fuel, which is the underlying source of data for both of the above."""

##################################################################

## DATA SOURCE:  update date in url!!!!
# http://content.caiso.com/green/renewrpt/20150222_DailyRenewablesWatch.txt


###############################################################


# TODO: separate function, called by seeding.py, for initial database seeding using scraper data.
# update the url to use, by iterating over a range of dates.
def initial_db_seeding():
    print "this is linked to seeding.py file"




# This is the task that runs each day, once per day, to update database.
def daily_scraper_db_update():
    yesterday = datetime.date.today() - datetime.timedelta(1)
    url_date = yesterday.strftime('%Y%m%d')
    get_historic_mw_by_fuel(url_date)

    ## TODO: check values within expected bounds, confirm timestamp is new, and update into db of dynamic data




# This is aseparate function for the CAISO web scraping renewables mw.
def get_historic_mw_by_fuel(date):
    current = datetime.datetime.now()
    current_str = str(current)

    try:
        url_file = "http://content.caiso.com/green/renewrpt/"+date+"_DailyRenewablesWatch.txt"
        count_lines = 1
        for line in urllib2.urlopen(url_file):
            if count_lines>2 and count_lines<27:
                data = line.split()
                hour, geotherm, biomass, biogas, small_hydro, wind, solar = data[0], data[1], data[2], data[3], data[4], data[5], data[6]
                print hour
            if count_lines >30:
                data = line.split()
                hour, nuclear, thermal, hydro = data[0], data[2], data[3], data[5]
                print hour
            count_lines+=1

    except:
        print ("Error. CAISO_hrly_data_scraper failure at",current_str)

        f = open('log_file.txt','a')
        f.write("\nError.  CAISO_hrly_data_scraper failure at: " +current_str)
        f.close



if __name__ == "__main__":
    daily_scraper_db_update()
