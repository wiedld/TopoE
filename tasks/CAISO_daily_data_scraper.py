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


##  DATES USED:  database was seeded on 2/24/2015.
#      therefore, used daily task to web scrap 2/23 data (20150223).
#      and used this funct below to seed 1/1/2014 thru 2/22/2015.
#           last day seeded is enddate -1.   make enddate = 20150223
def initial_db_seeding(startdate,enddate):
    """This function will be called by the seeding.py file in the parent directory.  For initial db seeding."""

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


def daily_scraper_db_update():
    """This is the task that runs each day, once per day, to update database."""

    yesterday = date.today() - timedelta(1)
    url_date = yesterday.strftime('%Y%m%d')
    get_historic_mw_by_fuel(url_date)

    ##TODO: confirm that exactly 216 records were added each day (24 hrs x 9 fuel_type).  Functional test.


###############################################################


## THESE TWO FUNCTIONS ARE USED FOR BOTH THE INITIAL SEEDING, AND THE DAILY DATABASE UPDATE (automated task).



def get_historic_mw_by_fuel(date):
    """This is a separate function for the CAISO web scraping renewables mw.  Logs errors.  Feeds scraped data to insert_row_db()."""

    current = datetime.now()
    current_str = str(current)

    try:
        url_file = "http://content.caiso.com/green/renewrpt/"+date+"_DailyRenewablesWatch.txt"

        count_lines = 1
        for line in urllib2.urlopen(url_file):
            fuel_mw = {}    # empty dict each time.
            if count_lines>2 and count_lines<27:
                data = line.split()
                fuel_mw['geotherm'] = int(data[1])
                fuel_mw['biomass'] = int(data[2])
                fuel_mw['biogas'] = int(data[3])
                fuel_mw['small_hydro'] = int(data[4])
                fuel_mw['wind'] = int(data[5])
                fuel_mw['solar'] = int(data[6])
                fuel_mw['thermal'] = int(data[7])
                hour = int(data[0])
                insert_row_db(date, hour, fuel_mw)

            if count_lines >30:
                data = line.split()
                fuel_mw['other_renewables'] = int(data[1])
                fuel_mw['nuclear'] = int(data[2])
                fuel_mw['thermal'] = int(data[3])
                fuel_mw['imports'] = int(data[4])
                fuel_mw['hydro'] = int(data[5])
                hour = int(data[0])
                insert_row_db(date, hour, fuel_mw)

            count_lines+=1


    except:
        print ("Error. CAISO_hrly_data_scraper failure at",current_str)

        f = open('tasks/logs/log_file.txt','a')
        f.write("\nError.  CAISO_daily_data_scraper failure at: " +current_str+" for date "+date)
        f.close
        # TODO: write a timeout funtion (delay), and recall function attempt again...call the main function (daily_scraper_db_update)?  Python library -- try up to x times until succeeds, and then would error and print to log file.  Once production -- use trigger email (make http request to email service, for fee).





def insert_row_db(date, hr, adict):
    """imports model, and inserts web scraped data into the db"""

    # add parent directory to the path, so can import model.py
    #  need model in order to update the database when this task is activated by cron
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)
    print parentdir
    import model
    print "model imported"
    session = model.connect()


    for k,v in adict.items():
        fuel_obj = model.HistoricCAISOProdByFuel()

        fuel_obj.date = datetime.strptime(date,'%Y%m%d')
        fuel_obj.hour = hr
        fuel_obj.fuel_type = k
        fuel_obj.mw_gen = v

        session.add(fuel_obj)

    session.commit()

    print ("Inserted data for date: "+date+" and hour: "+str(hr))



#####################################################################


if __name__ == "__main__":
    """cron task, called daily, will activate this"""
    daily_scraper_db_update()

