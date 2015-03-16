from datetime import datetime, timedelta
from pandas import DataFrame, merge, Series


import numpy as np
from array import array
import sklearn
from sklearn import svm
from sklearn.linear_model import LinearRegression

est = LinearRegression(fit_intercept=False)


#############################################################
#############################################################
# TODO;   was told good design used a class for linear regression.
#  need to incorporate this class, into the rest of the code.

class CAISO_hrly_ML(object):
    def __init__(self, x_vars, y_var1, y_var2, y_var3):
        # data for 2014, time_startly, for:
            # solar, wind, nuclear, hydro, demand, net imports
        self.available_in_RT = x_vars

        # data for jan-feb 2015, time_startly, for:
        self.need_predict_1 = y_var1    # nuclear
        self.need_predict_2 = y_var2    # hydro
        self.need_predict_3 = y_var3    # other


#############################################################
#############################################################

def predict_current_mix(solar, wind, demand):
    """using the CAISO values avilable every 5-10 minutes, and the coeffs found by multivariable linear regression models (hourly and monthly data), the outcome predict the total fuel mix displayed on the frontend: gas, coal, solar, wind, nuclear, hydro, other."""

    pass





#############################################################
#############################################################

# get 2014 data for x_vars, convert into np array

# note -- the HistoricCAISO ProdByFuel is Hour Beginning time
def getting_coeff_with_hrly_data():

    solar_series = query_CAISOProdByFuel_Series('solar')
    wind_series = query_CAISOProdByFuel_Series('wind')
    nuclear_series = query_CAISOProdByFuel_Series('nuclear')
    hydro_series = query_CAISOProdByFuel_Series('hydro')
    demand_series = query_CAISODemand_hrly_Series()
    imports_series = query_CAISONetImports_hrly_Series()
    # series will index on datetime

    #########################################
    # using x1,x2,x3,x4 = solar, wind, demand.  y= nuclear

    # combine series into table with column headers = x vars
    x_vars_dict = {'solar': solar_series,
                    'wind': wind_series,
                    'demand':demand_series
                    }

    df_x_vars = DataFrame(x_vars_dict)
    # print df_x_vars

    #### PREDICTING NUCLEAR #####
    # get series with y values
    series_y_var = nuclear_series
    # print series_y_var

    Y = np.asarray(series_y_var)
    X = np.asarray(df_x_vars)

    print "PREDICTING NUCLEAR"
    print "shape X", X.shape
    print "shape y", Y.shape

    print "est.fit(X, Y)", est.fit(X,Y)
    print "est.coef_", est.coef_

    #### OUTCOME ####
        # PREDICTING NUCLEAR
        # shape X (8706, 3)
        # shape y (8706,)
        # est.fit(X, Y) LinearRegression(copy_X=True, fit_intercept=False, normalize=False)
        # est.coef_ [ 0.06342347  0.14062451  0.04103758]

    #### PREDICTING HYDRO #####
    # get series with y values
    series_y_var_2 = hydro_series

    Y2 = np.asarray(series_y_var_2)

    print "PREDICTING HYDRO"
    print "shape X", X.shape
    print "shape y", Y2.shape

    # print "est.fit(X, Y)", est.fit(X,Y2)
    print "est.coef_", est.coef_

    #### OUTCOME ####
        # PREDICTING HYDRO
        # shape X (8706, 3)
        # shape y (8706,)
        # est.fit(X, Y) LinearRegression(copy_X=True, fit_intercept=False, normalize=False)
        # est.coef_ [ 0.03625611  0.1619504   0.15142367]





def getting_coeff_with_mo_data():
    #### PREDICTING COAL ###
    solar_mo_series = query_EIA_fuel_monthly_Series('solar')
    wind_mo_series = query_EIA_fuel_monthly_Series('wind')
    nuclear_mo_series = query_EIA_fuel_monthly_Series('nuclear')
    hydro_mo_series = query_EIA_fuel_monthly_Series('hydro')
    coal_mo_series = query_EIA_fuel_monthly_Series('coal')
    other_mo_series = query_EIA_fuel_monthly_Series('other')
        # not including gas, as it is the resource which changes the most through a given day.
        # therefore, when we breakdown the total fuel mix as a part of the total demand....we'll leave gas as the remainder serving the load until the peak daily curve.  Fits reality.

     #########################################
    # using x1,x2,x3,x4 = solar, wind, nuclear, hydro. y=coal.

    # combine series into table with column headers = x vars
    x_vars_dict = {'solar': solar_mo_series,
                    'wind': wind_mo_series,
                    'nuclear': nuclear_mo_series,
                    'hydro': hydro_mo_series
                    }

    df_x_vars = DataFrame(x_vars_dict)
    # print df_x_vars

    #### PREDICTING COAL #####
    # get series with y values
    series_y_var = coal_mo_series

    Y = np.asarray(series_y_var)
    X = np.asarray(df_x_vars)

    print "PREDICTING COAL"
    print "shape X", X.shape
    print "shape y", Y.shape

    print "est.fit(X, Y)", est.fit(X,Y)
    print "est.coef_", est.coef_

    # PREDICTING COAL
    # shape X (11, 4)
    # shape y (11,)
    # est.fit(X, Y) LinearRegression(copy_X=True, fit_intercept=False, normalize=False)
    # est.coef_ [ 0.03143584 -0.01411826  0.08017906 -0.01542515]

    #########################################
    # using x1,x2,x3,x4 = solar, wind, nuclear, hydro. y=other.

    # combine series into table with column headers = x vars
    x_vars_dict = {'solar': solar_mo_series,
                    'wind': wind_mo_series,
                    'nuclear': nuclear_mo_series,
                    'hydro': hydro_mo_series
                    }

    df_x_vars = DataFrame(x_vars_dict)
    # print df_x_vars

    #### PREDICTING OTHER #####
    # get series with y values
    series_y_var_2 = other_mo_series

    Y2 = np.asarray(series_y_var_2)
    X = np.asarray(df_x_vars)

    print "PREDICTING OTHER"
    print "shape X", X.shape
    print "shape y", Y2.shape

    print "est.fit(X, Y)", est.fit(X,Y2)
    print "est.coef_", est.coef_

    # PREDICTING OTHER
    # shape X (11, 4)
    # shape y (11,)
    # est.fit(X, Y) LinearRegression(copy_X=True, fit_intercept=False, normalize=False)
    # est.coef_ [-0.40502221  0.83684296  0.81505163  0.2379201 ]





#############################################################
#############################################################
# for each of the DBs, how to extract data and place in Series


def query_CAISOProdByFuel_Series(ea_fuel):
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

    import model
    print "model imported"
    s = model.connect()

    ea_fuel_obj = s.execute('SELECT time_start, fuel_type, mw_gen FROM HistoricCAISOProdByFuels WHERE fuel_type="%s" and time_start between "2014-01-01 07:00:00.000000" and "2015-01-01 00:00:00.000000"  ' % ea_fuel)
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





def query_CAISODemand_hrly_Series():
    """specifically gets demand data"""

    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

    import model
    print "model imported"
    s = model.connect()

    demand_obj = s.execute('SELECT time_start, mw_demand FROM HistoricCAISODemands WHERE CAISO_tac="CA ISO-TAC" and time_start between "2014-01-01 07:00:00.000000" and "2015-01-01 00:00:00.000000" ')
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





def query_CAISONetImports_hrly_Series():
    """specifically gets import data"""

    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

    import model
    print "model imported"
    s = model.connect()

    imports_obj = s.execute('SELECT time_start, sum(mw_imports) FROM HistoricCAISONetImports where time_start between "2014-01-01 07:00:00.000000" and "2015-01-01 00:00:00.000000" GROUP BY time_start ')
    imports_entry = imports_obj.fetchall()
    imports_df = DataFrame(imports_entry)
    imports_df.columns = ['time_start','mw_demand']

    dict_with_datetime_keys = { }

    for idx,row in enumerate(imports_df.values):
        time_start = row[0]

        # check date, since logs show we're missing a few
        if check_if_bad_date(time_start)!=True:

            # turn dict into a series.  will auto-index on dict keys
            mw_imports = row[1]
            dict_with_datetime_keys[time_start] = mw_imports

    return Series(dict_with_datetime_keys)





def query_EIA_fuel_monthly_Series(ea_fuel):
    """specifically gets EIA data from ProdGen"""

    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

    import model
    print "model imported"
    s = model.connect()

    fuel_codes = {
    'coal': '("BIT","ANT","LIG","SUB","RC","WC","CBL","SC", "SGC")',
    'gas': '("NG","BFG","OG","PG","OTH")',
    'nuclear': "NUC",
    'solar':"SUN",
    'hydro':"WAT",
    'wind':"WND",
    'other': '("DFO","RFO","JF","KER","WO","PC","SG","AB","MSW","OBS","WDS","OBL","SLW","BLQ","WDL","OBG","GEO","LFG","TDF","MSB","MSN","WH","PUR","SGP","MWH")'}

    if (ea_fuel=='nuclear') or (ea_fuel=='solar') or (ea_fuel=='wind') or (ea_fuel == 'hydro'):
        code = fuel_codes[ea_fuel]
        mo_fuel_obj = s.execute('SELECT sum(jan_mwh_gen), sum(feb_mwh_gen), sum(mar_mwh_gen), sum(apr_mwh_gen), sum(may_mwh_gen), sum(jun_mwh_gen), sum(jul_mwh_gen), sum(aug_mwh_gen), sum(sep_mwh_gen), sum(oct_mwh_gen), sum(nov_mwh_gen) FROM ProdGens WHERE fuel_type="%s" and state="CA" ' % code)

    if (ea_fuel=='coal') or (ea_fuel=='gas') or (ea_fuel=='other'):
        list_of_codes = fuel_codes[ea_fuel]
        mo_fuel_obj = s.execute('SELECT sum(jan_mwh_gen), sum(feb_mwh_gen), sum(mar_mwh_gen), sum(apr_mwh_gen), sum(may_mwh_gen), sum(jun_mwh_gen), sum(jul_mwh_gen), sum(aug_mwh_gen), sum(sep_mwh_gen), sum(oct_mwh_gen), sum(nov_mwh_gen) FROM ProdGens WHERE state="CA" and fuel_type IN %s ' % list_of_codes )

    mo_fuel_entry = mo_fuel_obj.fetchall()

    # turn into dict
    list_of_months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov']
    mo_fuel_entry_dict ={}
    for i in range(11):
        mo_fuel_entry_dict[list_of_months[i]] = mo_fuel_entry[0][i]

    # can now turn dict into Series
    return Series(mo_fuel_entry_dict)





def check_if_bad_date(datetime_obj_as_str):
    """certain dates are missing in CAISO fuel prod data.  exclude those dates"""

    # example index from pandas df:  2015-03-10 04:00:00.000000
    datetime_list = datetime_obj_as_str.split(" ")

    date_to_ck = datetime_list[0]
    bad_dates = ['2014-03-09', '2014-05-21', '2015-03-08', '2015-02-28', '2015-03-01', '2015-03-02', '2015-03-03', '2015-03-04', '2015-03-05', '2015-03-06', '2015-03-07', '2015-03-08', '2015-03-09', '2015-03-10' ]

    if date_to_ck in bad_dates:
        return True

    timestamp = datetime_list[1] # 04:00:00.000000
    time_as_list = timestamp.split(":")
    time_to_ck = time_as_list[1] # get the minutes

    if time_to_ck != "00":
        return True

    return False



#############################################################
#############################################################

if __name__ == "__main__":
    # getting_coeff_with_hrly_data()
    getting_coeff_with_mo_data()
    # query_EIA_fuel_monthly_Series('wind')





