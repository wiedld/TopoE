
from datetime import datetime, date, timedelta
from urllib2 import Request, urlopen, URLError

import zipfile
import os.path
import os
from xml.dom import minidom


test = "CAISO api for RT demand, is connected"


####################################################################

"""This file is used to update the database table: HistoricCAISODemand.

    There are two basic tasks this file contains:
    (1) inital seeding of the db using many dates (hourly data for each date).

    (2) a recurring task each day.  To update the latest hourly data.

    There is also a caiso_api_call function, which is the underlying source of data for both of the above."""

####################################################################
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
####################################################################
# INITIAL SEEDING OF DB

def initial_db_seeding(seed_startdate,seed_enddate):
    """This function will be called by the seeding.py file in the parent directory.  For initial db seeding."""

    # since this function is called from seeding.py, import datetime libraries as need to iterate over daterange for seeding.
    from datetime import datetime, timedelta
    start_loop = datetime.strptime(startdate,'%Y%m%d')
    end_loop = datetime.strptime(enddate,'%Y%m%d')

    for single_date in daterange(start_loop, end_loop):
        url_startdate = single_date.strftime('%Y%m%d')
        url_enddate = (single_date + timedelta(1)).strftime('%Y%m%d')
        get_realtime_api_data(url_startdate, url_enddate)



def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


##################################################################
# DAILY API, DAILY UPDATE OF DB

def daily_api_update():
    """This function will be called by the daily task (cron), to update demand in the db"""
    # update based on flask triggers
    pass

    # yesterday = date.today() - timedelta(1)
    # url_startdate = yesterday.strftime('%Y%m%d')
    # url_enddate = date.today().strftime('%Y%m%d')
    # get_realtime_api_data(url_startdate, url_enddate)


###################################################################
# BELOW FUNCTIONS ARE USED FOR BOTH OF THE TASKS SUMMARIZED ABOVE


def get_realtime_api_data(api_startdate, api_enddate):
    from datetime import datetime
    current = datetime.now()
    current_str = str(current)

    try:
        # note that is GMT time.  use T0:700 for now.
        # TODO: update for Daylight Savings time
        url = "http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=RTM&execution_type=RTD&startdatetime="+api_startdate+"T07:00-0000&enddatetime="+api_enddate+"T07:00-0000&version=1&as_region=ALL"

        # API call, downloads and saves the zipped file.
        file_name = url.split('/')[-1]  # zipped filename

        # sometimes there is an error with the urlopen(url)
        try:
            u = urlopen(url)
            file_path = "tasks/tmp/"+str(file_name) # what path to use
            # file_path = file_name
            f = open(file_path, 'wb')
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
            f.close()

            # unzip/extract file
            zfile = zipfile.ZipFile(file_path, "r")
            for name in zfile.namelist():
                (dirname, file_name) = os.path.split(name)
                zfile.extract(name, dirname)

            # open xml file and parse the data, inserting into list of dicts.
            xml_dom = minidom.parse(str(name))
            data = []
            for node in xml_dom.getElementsByTagName("REPORT_DATA"):
                # TODO:  make hour and minutes
                data.append({
                    'opr_date': handleTok(node.getElementsByTagName("OPR_DATE")),
                    # 'hour': handleTok(node.getElementsByTagName("INTERVAL_NUM")),
                    'CAISO_tac': handleTok(node.getElementsByTagName("RESOURCE_NAME")),
                    'mw_demand': handleTok(node.getElementsByTagName("VALUE"))
                    })
            print data

            ## TODO: check values within expected bounds, confirm timestamp is new, and update into db of dynamic data
            insert_row_db(api_startdate, data)

        except:
            print ("Error.  CAISO_flask_api failure at",current_str)

            f = open('tasks/logs/log_file.txt','a')
            f.write("\nError.  CAISO_flask_api failure at: " +current_str+" for date "+api_startdate)
            f.close


    except URLError:
        print ("Error.  CAISO_flask_api failure at",current_str)

        f = open('tasks/logs/log_file.txt','a')
        f.write("\nError.  CAISO__flask_api failure at: " +current_str+" for date "+api_startdate)
        f.close





def insert_row_db(date, list_of_dicts):
    """Takes in a list of dicts, with each list item equal to a timepoint. inserts into HistoricCAISODemand"""

    # add parent directory to the path, so can import model.py
    #  need model in order to update the database when this task is activated by cron
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)
    print parentdir
    import model
    print "model imported"
    session = model.connect()

    from datetime import datetime

    for timept_dict in list_of_dicts:
        demand_obj = model.HistoricCAISODemand()

        opr_date = (timept_dict['opr_date']).strip()
        demand_obj.date = datetime.strptime(opr_date,'%Y-%m-%d')
        demand_obj.hour = int(timept_dict['hour'])
        demand_obj.CAISO_tac = (timept_dict['CAISO_tac']).strip()
        demand_obj.mw_demand = int(timept_dict['mw_demand'])

        session.add(demand_obj)
        print "added to session:", demand_obj.date, demand_obj.hour, demand_obj.CAISO_tac, demand_obj.mw_demand

    # session.commit()

    print ("Inserted data for date: "+date)





################################################################
# below functions are from stackoverflow, for getting text within xml child node

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def handleTok(tokenlist):
    texts = ""
    for token in tokenlist:
        texts += " "+ getText(token.childNodes)
    return texts

################################################################

if __name__ == "__main__":
    """cron task, called daily, will activate this"""
    daily_api_update()


