import datetime
from urllib2 import Request, urlopen, URLError

from modules import ElementTree as ET
import zipfile
from xml.dom import minidom


"""This file is used to update the database table: HistoricCAISODemand.

    There are two basic tasks this file contains:
    (1) inital seeding of the db using many dates (hourly data for each date).

    (2) a recurring task each day.  To update the latest hourly data.

    There is also a caiso_api_call function, which is the underlying source of data for both of the above."""

########################################################
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
# RENEW_FCST_ACT_MW

    # http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_REN_FCST&market_run_id=ACTUAL&startdatetime=20130919T07:00-0000&enddatetime=20130920T07:00-0000&version=1

    # <REPORT_DATA>
    # <DATA_ITEM>RENEW_FCST_ACT_MW</DATA_ITEM>
    # <OPR_DATE>2013-09-19</OPR_DATE>
    # <INTERVAL_NUM>2</INTERVAL_NUM>
    # <INTERVAL_START_GMT>2013-09-19T08:00:00-00:00</INTERVAL_START_GMT>
    # <INTERVAL_END_GMT>2013-09-19T09:00:00-00:00</INTERVAL_END_GMT>
    # <VALUE>-0.86949</VALUE>
    # <TRADING_HUB>NP15</TRADING_HUB>
    # <RENEWABLE_TYPE>Solar</RENEWABLE_TYPE>
    # </REPORT_DATA>


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

def initial_db_seeding(seed_startdate,seed_enddate):
    """This function will be called by the seeding.py file in the parent directory.  For initial db seeding."""

    # since this function is called from seeding.py, import datetime libraries as need to iterate over daterange for seeding.
    from datetime import datetime, timedelta
    start_loop = datetime.strptime(startdate,'%Y%m%d')
    end_loop = datetime.strptime(enddate,'%Y%m%d')

    for single_date in daterange(start_loop, end_loop):
        url_startdate = single_date.strftime('%Y%m%d')
        url_enddate = (single_date + timedelta(1)).strftime('%Y%m%d')
        get_historic_api_data(url_startdate, url_enddate)



def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


##################################################################


def daily_api_data(date):
    """This function will be called by the daily task (cron), to update demand in the db"""

    yesterday = date.today() - timedelta(1)
    url_startdate = yesterday.strftime('%Y%m%d')
    url_enddate = date.today().strftime('%Y%m%d')
    get_historic_api_data(url_startdate, url_enddate)


###################################################################
# BELOW FUNCTIONS ARE USED FOR BOTH OF THE TASKS SUMMARIZED ABOVE


def get_historic_api_data(api_startdate, api_enddate):
    current = datetime.datetime.now()
    current_str = str(current)

    #  TODO:  get api'ed file unzipped.  update api url with date.

    try:
        url = "http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=ACTUAL&startdatetime="+api_startdate+"T07:00-0000&enddatetime="+api_enddate+"T07:00-0000&version=1&as_region=ALL"


##############################
# paths/variables used in the different unzip methods (troubleshooting)

        response = urlopen("http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=ACTUAL&startdatetime=20140101T00:00-0000&enddatetime=20140102T00:00-0000&version=1&as_region=ALL")
        caiso_rt = response.read()
        # print ("api response:", caiso_rt)
        path = "http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=ACTUAL&startdatetime=20140101T07:00-0000&enddatetime=20140102T07:00-0000&version=1&as_region=ALL"
##############################
# works for plain xml.  not zipped

        # XML_tree = ET.parse(path)
        # root = tree.getroot()
##############################
# xmlstr = zipfile.read(path)
# AttributeError: 'module' object has no attribute 'read'

        # xmlstr = zipfile.read(path)
        # root = ET.fromstring(xmlstr)
        # print root
        # root.findall('VALUE')
#############################

# Creates a file.  But it contains non-XML.

        # file_name = url.split('/')[-1]  # zipped filename
        # print file_name
        # u = urlopen(url)
        # print u
        # f = open(file_name, 'wb')
        # meta = u.info()
        # print meta

        # file_size_dl = 0
        # block_sz = 8192
        # while True:
        #     buffer = u.read(block_sz)
        #     if not buffer:
        #         break

        #     file_size_dl += len(buffer)
        #     f.write(buffer)

        # f.close()

##################################################
# File "tasks/CAISO_api.py", line 113, in main
# zfolder = zipfile.ZipFile(path, "r")
# IOError: [Errno 2] No such file or directory: 'http://oasis.caiso.com/oasisapi/SingleZip?queryname=SLD_FCST&market_run_id=ACTUAL&startdatetime=20140101T07:00-0000&enddatetime=20140102T07:00-0000&version=1&as_region=ALL'


        # zfile = zipfile.ZipFile(path, "r")
        # for name in zfile.namelist():
        #     (dirname, filename) = os.path.split(name)
        #     xml = zfile.extract(name, dirname)
        #     xml = zfolder.read(zfile)
        #     xml_dom = minidom.parse(xml)
        #     print xml_dom

###############################################

# TODO:  below code is to use once we have the XML unzipped.
    # need to wire this in to the above xml generated above.

        xml_dom = minidom.parse("test.xml")
        # print xml_dom

        data = []
        for node in xml_dom.getElementsByTagName("REPORT_DATA"):
            data.append({
                'date': handleTok(node.getElementsByTagName("OPR_DATE")),
                'hour': handleTok(node.getElementsByTagName("INTERVAL_NUM")),
                'CAISO_tac': handleTok(node.getElementsByTagName("RESOURCE_NAME")),
                'mw_demand': handleTok(node.getElementsByTagName("VALUE"))
                })
        print data


         ## TODO: check values within expected bounds, confirm timestamp is new, and update into db of dynamic data

    except URLError:
        print ("Error.  CAISO_api failure at",current_str)

        f = open('/logs/ERROR_log_file.txt','a')
        f.write("\nError.  CAISO_api failure at: " +current_str)
        f.close


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
    get_historic_api_data('20140101', '20140102')


