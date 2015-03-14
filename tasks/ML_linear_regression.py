from datetime import datetime, timedelta
from pandas import DataFrame, merge, Series


import numpy as np
from array import array
import sklearn
from sklearn import svm
from sklearn.linear_model import LinearRegression

est = LinearRegression(fit_intercept=False)


class CAISO_hrly_ML(object):
    def __init__(self, x_vars, y_var1, y_var2, y_var3):
        # data for 2014, time_startly, for:
            # solar, wind, nuclear, hydro, demand, net imports
        self.available_in_RT = x_vars

        # data for jan-feb 2015, time_startly, for:
        self.need_predict_1 = y_var1    # nuclear
        self.need_predict_2 = y_var2    # hydro
        self.need_predict_3 = y_var3    # other



#####################################################

# get 2014 data for x_vars, convert into np array

# note -- the HistoricCAISO ProdByFuel is Hour Beginning time
def main():

    solar_series = query_db_fuel_Series('solar')
    wind_series = query_db_fuel_Series('wind')
    nuclear_series = query_db_fuel_Series('nuclear')
    hydro_series = query_db_fuel_Series('hydro')
    # series will index on datetime

    # combine series into table with column headers = x vars
    x_vars_dict = {'solar': solar_series,
                    'wind': wind_series,
                    'nuclear':nuclear_series,
                    'hydro': hydro_series}

    df_x_vars = DataFrame(x_vars_dict)
    print df_x_vars

    # get series with y values
    series_y_var = query_db_demand_Series()
    print series_y_var

    Y = np.asarray(series_y_var)
    X = np.asarray(df_x_vars)

    print "shape X", X.shape
    print "shape y", Y.shape

    print "est.fit(X, Y)", est.fit(X,Y)
    print "est.coef_", est.coef_







def query_db_fuel_Series(ea_fuel):
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

    import model
    print "model imported"
    s = model.connect()

    ea_fuel_obj = s.execute('SELECT time_start, fuel_type, mw_gen FROM HistoricCAISOProdByFuels WHERE fuel_type="%s" ' % ea_fuel)
    ea_fuel_entry = ea_fuel_obj.fetchall()
    ea_fuel_df = DataFrame(ea_fuel_entry)
    ea_fuel_df.columns = ['time_start', 'fuel_type', 'mw_gen']

    dict_with_datetime_keys = { }

    for idx,row in enumerate(ea_fuel_df.values):
        time_start = row[0]

        # check date, since logs show we're missing a few
        if check_if_bad_date(time_start)!=True:
            mw_gen = row[2]
            dict_with_datetime_keys[time_start] = mw_gen

    # turn dict into a series.  will auto-index on dict keys
    return Series(dict_with_datetime_keys)





def query_db_demand_Series():
    """specifically gets demand data"""

    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

    import model
    print "model imported"
    s = model.connect()

    demand_obj = s.execute('SELECT time_start, mw_demand FROM HistoricCAISODemands WHERE CAISO_tac="CA ISO-TAC" ')
    demand_entry = demand_obj.fetchall()
    demand_df = DataFrame(demand_entry)
    demand_df.columns = ['time_start','mw_demand']

    dict_with_datetime_keys = { }

    for idx,row in enumerate(demand_df.values):
        time_start = row[0]

        # check date, since logs show we're missing a few
        if check_if_bad_date(time_start)!=True:

            # turn dict into a series.  will auto-index on dict keys
            mw_demand = row[1]
            dict_with_datetime_keys[time_start] = mw_demand

    return Series(dict_with_datetime_keys)





def check_if_bad_date(datetime_obj_as_str):
    """certains dates are missing in CAISO fuel prod data.  exclude those dates"""

    # example index from pandas df:  2015-03-10 04:00:00.000000
    datetime_list = datetime_obj_as_str.split(" ")
    date_to_ck = datetime_list[0]
    bad_dates = ['2014-03-09', '2014-05-21', '2015-03-08']

    if date_to_ck in bad_dates:
        return True

    return False





if __name__ == "__main__":
    main()




#####################################################


    # log shows that the seeding dates which failed are: 20140309, 20140521, 20150308
    # bad_date_start = datetime.strptime('2014-03-09','%Y-%m-%d')
    # bad_date_end = datetime.strptime('2014-03-10','%Y-%m-%d')
    # bad_date_start_2 = datetime.strptime('2014-05-21','%Y-%m-%d')
    # bad_date_end_2 = datetime.strptime('2014-05-22','%Y-%m-%d')
    # bad_date_start_3 = datetime.strptime('2015-03-08','%Y-%m-%d')
    # bad_date_end_3 = datetime.strptime('2015-03-09','%Y-%m-%d')

    # if (datetime_obj>bad_date_start) and (datetime_obj<bad_date_end):
    #     return False
    # if (datetime_obj>bad_date_start_2) and (datetime_obj<bad_date_end_2):
    #     return False
    # if (datetime_obj>bad_date_start_3) and (datetime_obj<bad_date_end_3):
    #     return False

    # return True

