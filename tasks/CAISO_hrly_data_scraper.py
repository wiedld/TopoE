from datetime import datetime, date, timedelta
import urllib2


"""This file is used to update the database table: HistoricCAISOProdByFuels.

    There are two basic tasks this file contains:
    (1) inital seeding of the db using many dates (hourly data for each date).
    (2) a recurring task each day.  To update the latest hourly data.

    There is also a web scaper function, get_historic_mw_by_fuel, which is the underlying source of data for both of the above."""

##################################################################

## DATA SOURCE:  update date in url!!!!
# http://content.caiso.com/green/renewrpt/20150222_DailyRenewablesWatch.txt


###############################################################


#  This is a function, called by seeding.py, for initial database seeding using scraper data.
# It the url_date to use, by iterating over a range of dates.
def initial_db_seeding(startdate,enddate):
    """This function will be called by the seeding.py file in the parent directory."""

    # since this function is called from seeding.py, import datetime libraries as need to iterate over daterange for seeding.
    from datetime import datetime, timedelta
    start_loop = datetime.strptime(startdate,'%Y%m%d')
    end_loop = datetime.strptime(enddate,'%Y%m%d')

    for single_date in daterange(start_loop, end_loop):
        url_date = single_date.strftime('%Y%m%d')
        get_historic_mw_by_fuel(url_date)



def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


###############################################################

# This is the task that runs each day, once per day, to update database.
def daily_scraper_db_update():
    yesterday = date.today() - timedelta(1)
    url_date = yesterday.strftime('%Y%m%d')
    get_historic_mw_by_fuel(url_date)

    ## TODO: check values within expected bounds, confirm timestamp is new, and update into db of dynamic data


###############################################################


## THESE TWO FUNCTIONS ARE USED FOR BOTH THE INITIAL SEEDING, AND THE DAILY DATABASE UPDATE (automated task).


# This is a separate function for the CAISO web scraping renewables mw.  Logs errors.  Feeds scraped data to insert_row_db().
def get_historic_mw_by_fuel(date):
    current = datetime.now()
    current_str = str(current)

    try:
        url_file = "http://content.caiso.com/green/renewrpt/"+date+"_DailyRenewablesWatch.txt"
        count_lines = 1
        for line in urllib2.urlopen(url_file):
            if count_lines>2 and count_lines<27:
                data = line.split()
                hour, geotherm, biomass, biogas, small_hydro, wind, solar = data[0], data[1], data[2], data[3], data[4], data[5], data[6]
                insert_row_db(date, hour)
            if count_lines >30:
                data = line.split()
                hour, nuclear, thermal, hydro = data[0], data[2], data[3], data[5]
                insert_row_db(date, hour)
            count_lines+=1

    except:
        print ("Error. CAISO_hrly_data_scraper failure at",current_str)

        f = open('log_file.txt','a')
        f.write("\nError.  CAISO_hrly_data_scraper failure at: " +current_str)
        f.close



def insert_row_db(date, hr):
    # add parent directory to the path, so can import model.py
    #  need model in order to update the database when this task is activated by cron
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)
    import model

    print ("row would be inserted for date: "+date+" and hour: "+hr)

    ##  TODO:  session object, add, commit
    # fuel_object = model.HistoricCAISOProdByFuel()
    # id = Column(Integer, primary_key=True)
    # date = Column(DateTime)
    # hour = Column(Integer)
    # minute = Column(Integer)
    # fuel_type = Column(String(20))
    # mw_gen = Column(Integer)



if __name__ == "__main__":
    daily_scraper_db_update()
