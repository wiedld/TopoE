import datetime
import urllib2
from BeautifulSoup import BeautifulSoup


# This file should include web scrapping for two unique ids, cron every 10 minute.  Collects realtime data which updates every 10 minutes.


## DATA SOURCE:
# http://content.caiso.com/outlook/SP/renewables.html

# <span class="to_readings" id="totalrenewables">1919 MW</span>
# <span class="to_callout1">Current Solar:</span> <span class="to_readings" id="currentsolar">0 MW</span>
# <span class="to_callout1">Current Wind:</span> <span class="to_readings" id="currentwind">216 MW</span>

###############################################################
## POSSIBLE FUTURE DIRECTIONS:

# build a web scraper for 10 minute updates on actual demand, today's forecats peak, and tmrw's forecat peak?  10 minute updated...most current!
#  http://content.caiso.com/outlook/SP/systemconditions.html

##############################################################

test = "CAISO scraper for RT solar, wind, and demand is connected"


def get_solar_wind():
    current = datetime.datetime.now()
    current_str = str(current)

    try:
        soup = BeautifulSoup(urllib2.urlopen("http://content.caiso.com/outlook/SP/renewables.html").read())

        solar = soup.find(id="currentsolar")
        str_solar = solar.string
        wind = soup.find(id="currentwind")
        str_wind = wind.string
        mw_solar = int(str_solar.replace(" MW",""))
        mw_wind = int(str_wind.replace(" MW",""))

        return mw_solar, mw_wind

         ## TODO: check values within expected bounds, confirm timestamp is new, and update into db of dynamic data

    except:
        f = open('log_file.txt','a')
        f.write("\nError.  CAISO_solar-wind_data_scraper failure at: " +current_str)
        f.close



# //*[@id="currentsystemdemand"]


def get_demand():
    current = datetime.datetime.now()
    current_str = str(current)

    try:
        soup = BeautifulSoup(urllib2.urlopen("http://content.caiso.com/outlook/SP/systemconditions.html").read())

        demand = soup.find(id="currentsystemdemand")

        str_demand = demand.string
        mw_demand = int(str_demand.replace(" MW",""))

        print ("demand", mw_demand)

        return mw_demand

         ## TODO: check values within expected bounds, confirm timestamp is new, and update into db of dynamic data

    except:
        f = open('log_file.txt','a')
        f.write("\nError.  CAISO_demand_data_scraper failure at: " +current_str)
        f.close

#currentsystemdemand


if __name__ == "__main__":
    get_demand()
    get_solar_wind()

