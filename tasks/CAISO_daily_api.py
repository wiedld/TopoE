
from datetime import datetime, date, timedelta
from urllib2 import Request, urlopen, URLError

import zipfile
import os.path
import os
from xml.dom import minidom


"""This file is used to update two database tables: HistoricCAISODemands
    HistoricCAISONetImports

    There are two basic tasks this file contains:
    (1) inital seeding of the db using many dates (hourly data for each date).

    (2) a recurring task each day.  To update the latest hourly data.

    There are also two caiso_api_call functions, which are the underlying source of data for both of the above."""

####################################################################
## DATA SOURCE DOCUMENTATION:
# http://www.caiso.com/Documents/InterfaceSpecifications-OASIS_v4_2_4_Clean.pdf

####################################################################
##### WHAT IS USED for HistoricCAISODemands #############

# SYS_FCST_ACT_MW

    # http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=ACTUAL&startdatetime=20130919T07:00-0000&enddatetime=20130920T07:00-0000&version=1&as_region=ALL

    # <REPORT_DATA>
    # <DATA_ITEM>SYS_FCST_ACT_MW</DATA_ITEM>
    # <RESOURCE_NAME>CA ISO-TAC</RESOURCE_NAME>
    # <OPR_DATE>2013-09-19</OPR_DATE>
    # <INTERVAL_NUM>18</INTERVAL_NUM>
    # <INTERVAL_START_GMT>2013-09-20T00:00:00-00:00</INTERVAL_START_GMT>
    # <INTERVAL_END_GMT>2013-09-20T01:00:00-00:00</INTERVAL_END_GMT>
    # <VALUE>33493</VALUE>
    # </REPORT_DATA>


####################################################################
##### WHAT IS USED for HistoricCAISONetImports #############

# ENE_IMPORT_MW  (is from TRNS_CURR_USAGE)

    # "http://oasis.caiso.com/oasisapi/SingleZip?queryname=TRNS_CURR_USAGE&market_run_id=ACTUAL&startdatetime=20130919T07:00-0000&enddatetime=20130920T07:00-0000&version=1&as_region=ALL"

    # <REPORT_DATA>
    # <DATA_ITEM>ENE_IMPORT_MW</DATA_ITEM>
    # <SOURCE>COTPISO_ITC</SOURCE>
    # <RESOURCE_NAME>COTPISO_MSL</RESOURCE_NAME>
    # <DIRECTION>E</DIRECTION>
    # <OPR_DATE>2013-09-19</OPR_DATE>
    # <INTERVAL_NUM>24</INTERVAL_NUM>
    # <INTERVAL_START_GMT>2013-09-20T06:00:00-00:00</INTERVAL_START_GMT>
    # <INTERVAL_END_GMT>2013-09-20T07:00:00-00:00</INTERVAL_END_GMT>
    # <VALUE>0</VALUE>
    # </REPORT_DATA>

# note: there is no option for total CAISO.  only lists all of the interfaces



####################################################################
####################################################################
####################################################################
# INITIAL SEEDING OF DB

def initial_db_seeding(seed_startdate,seed_enddate):
    """This function will be called by the seeding.py file in the parent directory.  For initial db seeding."""

    # since this function is called from seeding.py, import datetime libraries as need to iterate over daterange for seeding.
    from datetime import datetime, timedelta
    start_loop = datetime.strptime(seed_startdate,'%Y%m%d')
    end_loop = datetime.strptime(seed_enddate,'%Y%m%d')

    for single_date in daterange(start_loop, end_loop):
        url_startdate = single_date.strftime('%Y%m%d')
        url_enddate = (single_date + timedelta(1)).strftime('%Y%m%d')

        get_historic_demand_api_data(url_startdate, url_enddate)

        # not using Net Imports now.  may use in the future
        # get_historic_imports_api_data(url_startdate, url_enddate)



def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


##################################################################
# DAILY API, DAILY UPDATE OF DB

def daily_api_update():
    """This function will be called by the daily task (cron), to update demand in the db"""

    yesterday = date.today() - timedelta(1)
    url_startdate = yesterday.strftime('%Y%m%d')
    url_enddate = date.today().strftime('%Y%m%d')

    get_historic_demand_api_data(url_startdate, url_enddate)

    # not using Net Imports now.  may use in the future
    # get_historic_imports_api_data(url_startdate, url_enddate)


###################################################################
# HISTORIC DEMAND
    # BELOW FUNCTIONS ARE USED FOR BOTH SEEDING & DAILY UPDATE


def get_historic_demand_api_data(api_startdate, api_enddate):
    from datetime import datetime
    current = datetime.now()
    current_str = str(current)

    try:
        # note that is GMT time.  use T0:700 for now.
        # TODO: update for Daylight Savings time
        url = "http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=ACTUAL&startdatetime="+api_startdate+"T07:00-0000&enddatetime="+api_enddate+"T07:00-0000&version=1&as_region=ALL"

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

                # slice out the date/time, start & end interval
                # u ' %Y-%m-%dT%H:%M:00-00:00'
                interval_start = (handleTok(node.getElementsByTagName("INTERVAL_START_GMT"))).encode("utf8").strip()
                interval_end = (handleTok(node.getElementsByTagName("INTERVAL_END_GMT"))).encode("utf8").strip()

                interval_start = interval_start[0:16]
                interval_end = interval_end[0:16]

                data.append({
                        'opr_date': (handleTok(node.getElementsByTagName("OPR_DATE"))).encode("utf8").strip(),
                        'time_start': datetime.strptime(interval_start,'%Y-%m-%dT%H:%M'),
                        'time_end': datetime.strptime(interval_end,'%Y-%m-%dT%H:%M'),
                        'caiso_tac': (handleTok(node.getElementsByTagName("RESOURCE_NAME"))).encode("utf8").strip(),
                        'mw_demand': (handleTok(node.getElementsByTagName("VALUE"))).encode("utf8").strip()
                        })

             ## TODO: check values within expected bounds, confirm timestamp is new, and update into db of dynamic data

            insert_row_demand_db(api_startdate, data)


        except:
            f = open('tasks/logs/log_file.txt','a')
            f.write("\nError.  CAISO_daily_api, Demand data, failure at: " +current_str+" for date "+api_startdate)
            f.close

    except URLError:
        f = open('tasks/logs/log_file.txt','a')
        f.write("\nError.  CAISO_daily_api, Demand data, failure at: " +current_str+" for date "+api_startdate)
        f.close





def insert_row_demand_db(date, list_of_dicts):
    """Takes in a list of dicts, with each list item equal to a timepoint. inserts into HistoricCAISODemand"""

    # add parent directory to the path, so can import model.py
    #  need model in order to update the database when this task is activated by cron

    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

    import model
    session = model.connect()

    from datetime import datetime

    for timept_dict in list_of_dicts:
        print timept_dict
        demand_obj = model.HistoricCAISODemand()

        opr_date = timept_dict['opr_date']
        demand_obj.date = datetime.strptime(opr_date,'%Y-%m-%d')

        demand_obj.time_start = timept_dict['time_start']
        demand_obj.time_end = timept_dict['time_end']
        demand_obj.caiso_tac = (timept_dict['caiso_tac']).strip()
        demand_obj.mw_demand = int(timept_dict['mw_demand'])

        session.add(demand_obj)

    session.commit()

    # print ("Inserted Demand data for date: "+date)



###################################################################
# HISTORIC NET IMPORTS
    # BELOW FUNCTIONS ARE USED FOR BOTH SEEDING & DAILY UPDATE

###### DECISION POINT #######
    # the origin point of examining this data is to look for trends and can be applied in realtime.
    # However, this data takes a long time to download each time, so may not be a good predictor in realtime.  There may be another creative use in the future.  But not for now, and not while planning for Hackbright Career Day.

def get_historic_imports_api_data(api_startdate, api_enddate):
    from datetime import datetime
    current = datetime.now()
    current_str = str(current)

    try:
        # note that is GMT time.  use T0:700 for now.
        # TODO: update for Daylight Savings time
        url = "http://oasis.caiso.com/oasisapi/SingleZip?queryname=TRNS_CURR_USAGE&market_run_id=ACTUAL&startdatetime="+api_startdate+"T07:00-0000&enddatetime="+api_enddate+"T07:00-0000&version=1&as_region=ALL"

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

                # only get the report for ENE_IMPORT_MW
                report_type = (handleTok(node.getElementsByTagName("DATA_ITEM"))).encode("utf8").strip()
                if report_type=='ENE_IMPORT_MW':

                    # slice out the date/time, start & end interval
                    # u ' %Y-%m-%dT%H:%M:00-00:00'
                    interval_start = (handleTok(node.getElementsByTagName("INTERVAL_START_GMT"))).encode("utf8").strip()
                    interval_end = (handleTok(node.getElementsByTagName("INTERVAL_END_GMT"))).encode("utf8").strip()

                    interval_start = interval_start[0:16]
                    interval_end = interval_end[0:16]

                    data.append({
                        'opr_date': (handleTok(node.getElementsByTagName("OPR_DATE"))).encode("utf8").strip(),
                        'time_start': datetime.strptime(interval_start,'%Y-%m-%dT%H:%M'),
                        'time_end': datetime.strptime(interval_end,'%Y-%m-%dT%H:%M'),
                        'resource': (handleTok(node.getElementsByTagName("RESOURCE_NAME"))).encode("utf8").strip(),
                        'mw_imports': (handleTok(node.getElementsByTagName("VALUE"))).encode("utf8").strip()
                        })

             ## TODO: check values within expected bounds, confirm timestamp is new, and update into db of dynamic data

            insert_row_imports_db(api_startdate, data)


        except:
            f = open('tasks/logs/log_file.txt','a')
            f.write("\nError.  CAISO_daily_api, Imports data, failure at: " +current_str+" for date "+api_startdate)
            f.close

    except URLError:
        f = open('tasks/logs/log_file.txt','a')
        f.write("\nError.  CAISO_daily_api, Imports data, failure at: " +current_str+" for date "+api_startdate)
        f.close





def insert_row_imports_db(date, list_of_dicts):
    """Takes in a list of dicts, with each list item equal to a timepoint. inserts into HistoricCAISODemand"""

    # add parent directory to the path, so can import model.py
    #  need model in order to update the database when this task is activated by cron

    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

    import model
    session = model.connect()

    from datetime import datetime

    for timept_dict in list_of_dicts:
        imports_obj = model.HistoricCAISONetImport()

        opr_date = timept_dict['opr_date']
        imports_obj.date = datetime.strptime(opr_date,'%Y-%m-%d')

        imports_obj.time_start = timept_dict['time_start']
        imports_obj.time_end = timept_dict['time_end']

        imports_obj.resource = (timept_dict['resource']).strip()

        imports_obj.mw_imports = float(timept_dict['mw_imports'])

        session.add(imports_obj)

    session.commit()

    # print ("Inserted Imports data for date: "+date)





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


