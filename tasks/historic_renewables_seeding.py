import datetime
import urllib2
from BeautifulSoup import BeautifulSoup


# use web scraping to populate historical data for all renewables using the base url (with date portion of the url updated during looped -- with date iteration -- during seeding).


## DATA SOURCE:  update date in url!!!!
# http://content.caiso.com/green/renewrpt/20150222_DailyRenewablesWatch.txt

# <span class="to_readings" id="totalrenewables">1919 MW</span>
# <span class="to_callout1">Current Solar:</span> <span class="to_readings" id="currentsolar">0 MW</span>
# <span class="to_callout1">Current Wind:</span> <span class="to_readings" id="currentwind">216 MW</span>

###############################################################



def main():
    current = datetime.datetime.now()
    current_str = str(current)

    try:
        url_file = "http://content.caiso.com/green/renewrpt/20150222_DailyRenewablesWatch.txt"
        # url_file = "http://content.caiso.com/green/renewrpt/%Y%m%d_DailyRenewablesWatch.txt"
        count_lines = 1
        for line in urllib2.urlopen(url_file):
            if count_lines>2 and count_lines<27:
                data = line.split()
                geotherm, biomass, biogass, small_hydro, wind, solar = data[1], data[2], data[3], data[4], data[5], data[6]
                print "wind", wind
                print "solar", solar
            if count_lines >30:
                data = line.split()
                nuclear, thermal, hydro = data[2], data[3], data[5]
                print "nuclear", nuclear
                print "hydro", hydro
            count_lines+=1
         ## TODO: check values within expected bounds, confirm timestamp is new, and update into db of dynamic data

    except:
        print ("Error with historic_renewables_seeding at",current_str)

        f = open('log_file.txt','a')
        f.write("\nError.  historic_renewables_seeding failure at: " +current_str)
        f.close



if __name__ == "__main__":
    main()
