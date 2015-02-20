import datetime
import urllib2
from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(urllib2.urlopen("http://content.caiso.com/outlook/SP/renewables.html").read())



# This file should include web scrapping for two unique ids, cron every 10 minute.  Collects realtime data which updates every 10 minutes.


## DATA SOURCE:
# http://content.caiso.com/outlook/SP/renewables.html

# <span class="to_readings" id="totalrenewables">1919 MW</span>
# <span class="to_callout1">Current Solar:</span> <span class="to_readings" id="currentsolar">0 MW</span>
# <span class="to_callout1">Current Wind:</span> <span class="to_readings" id="currentwind">216 MW</span>

###############################################################



def main():
    current = datetime.datetime.now()
    current_str = str(current)

    try:
        solar = soup.find(id="currentsolar")
        str_solar = solar.string
        wind = soup.find(id="currentwind")
        str_wind = wind.string
        mw_solar = int(str_solar.replace(" MW",""))
        mw_wind = int(str_wind.replace(" MW",""))
        print ("solar:", mw_solar)
        print ("wind:", mw_wind)
         ## TODO: update into db of dynamic data

    except:
        print ("Error.  CAISO web scraper failure at",current_str)

        f = open('log_file.txt','a')
        f.write("\nError.  CAISO web scraper failure at: " +current_str)
        f.close



if __name__ == "__main__":
    main()

