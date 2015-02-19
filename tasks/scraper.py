import datetime
import requests
import lxml.html

# This file should include web scrapping for two unique ids, cron every 10 minute.  Collects realtime data which updates every 10 minutes.


## DATA SOURCE:
# http://content.caiso.com/outlook/SP/renewables.html 

# <span class="to_readings" id="totalrenewables">1919 MW</span>
# <span class="to_callout1">Current Solar:</span> <span class="to_readings" id="currentsolar">0 MW</span>
# <span class="to_callout1">Current Wind:</span> <span class="to_readings" id="currentwind">216 MW</span>

###############################################################


# TODO.  github this over to my machine.  update env, install lxml (requires libxml2 2.9.0+ and libxslt 1.1.26+).  Then try the below code and troubleshoot.

def main():
    current = datetime.datetime.now()
    cur_str = str(current)
    try:
        html = requests.get("http://content.caiso.com/outlook/SP/renewables.html").content
        dom = lxml.html.fromstring(html)
        mw_solar = dom.cssselect('.currentsolar') 
        mw_wind = dom.cssselect('.currentwind')
        ## TODO: update into db of dynamic data
        print ("solar:", mw_solar)
        print ("wind:", mw_wind)
    except:
        print ("Error.  CAISO web scrape failure at",cur_str)


if __name__ == "__main__":
    main()

    