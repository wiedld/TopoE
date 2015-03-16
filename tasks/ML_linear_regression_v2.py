from datetime import datetime, timedelta
from pandas import DataFrame, merge, Series


import numpy as np
from array import array
import sklearn
from sklearn import svm
from sklearn.linear_model import LinearRegression

estA = LinearRegression(fit_intercept=True)
estB = LinearRegression(fit_intercept=True)
est1 = LinearRegression(fit_intercept=True)
est2 = LinearRegression(fit_intercept=True)
est3 = LinearRegression(fit_intercept=True)
est4 = LinearRegression(fit_intercept=True)
est5 = LinearRegression(fit_intercept=True)
est6 = LinearRegression(fit_intercept=True)

#############################################################
#############################################################
# TODO;   was told good design used a class for linear regression.
#  need to incorporate this class, into the rest of the code.

# class CAISO_hrly_ML(object):
#     def __init__(self, x_vars, y_var1, y_var2, y_var3):
#         # data for 2014, time_startly, for:
#             # solar, wind, nuclear, hydro, demand, net imports
#         self.available_in_RT = x_vars

#         # data for jan-feb 2015, time_startly, for:
#         self.need_predict_1 = y_var1    # nuclear
#         self.need_predict_2 = y_var2    # hydro
#         self.need_predict_3 = y_var3    # other


#############################################################
#############################################################

def predict_current_mix(solar, wind, demand):
    """using the CAISO values avilable every 5-10 minutes, and the coeffs found by multivariable linear regression models (monthly data), the outcome predict the total fuel mix displayed on the frontend: gas, coal, solar, wind, nuclear, hydro, other."""

    # correlation built from hrly data
    hydro = predict_using_hrly_data(solar, wind, demand)

    # correlation built from monthly data
    gas,coal,nuclear,other = predict_using_mo_data(solar,wind,hydro,demand)

    curr_fuel_mix_prediction = {
        'gas': round(gas),
        'coal': round(coal),
        'solar': round(solar),
        'wind': round(wind),
        'nuclear': round(nuclear),
        'hydro': round(hydro),
        'other': round(other)
    }

    print demand
    print curr_fuel_mix_prediction




#############################################################
#############################################################

# get 2014 data for x_vars, convert into np array

# note -- the HistoricCAISO ProdByFuel is Hour Beginning time
def predict_using_hrly_data(curr_solar, curr_wind, curr_demand):
    """this prediction is not used in the final model.  Because the demand, solar, and wind are extremely variable throughout a given day and are not great predictors for the more stable nuclear and hydro.  Was receiving very illogical results...more volatile than reality."""

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

    #### PREDICTING HYDRO #####
    # get series with y values
    series_y_var = hydro_series
    # print series_y_var

    Ya = np.asarray(series_y_var)
    Xa = np.asarray(df_x_vars)

    print "PREDICTING HYDRO"
    print "shape X", Xa.shape
    print "shape y", Ya.shape

    print "est.fit(X, Y)", estA.fit(Xa,Ya)
    print "est.coef_", estA.coef_

    curr_dict_A = {'solar':curr_solar, 'wind':curr_wind, 'demand':curr_demand}
    curr_series_A = Series(curr_dict_A)
    curr_input_A = np.asarray(curr_series_A)

    hydro_prediction = estA.predict(curr_input_A)
    print "hydro_prediction", hydro_prediction


    # # #### PREDICTING NUCLEAR #####
    # x_vars_dict = {'solar': solar_series,
    #                 'wind': wind_series,
    #                 'demand':demand_series,
    #                 'hydro': hyd
    #                 }

    # df_x_vars = DataFrame(x_vars_dict)

    # # get series with y values
    # series_y_var_b = hydro_series

    # Yb = np.asarray(series_y_var_b)

    # print "PREDICTING HYDRO"
    # print "shape X", Xb.shape
    # print "shape y", Yb.shape

    # print "est.fit(X, Y)", estB.fit(Xb,Yb)
    # print "est.coef_", estB.coef_

    # curr_dict_A = {'solar':curr_solar, 'wind':curr_wind, 'demand':curr_demand, 'hydro':hydro_prediction}
    # curr_series_A = Series(curr_dict_A)
    # curr_input_A = np.asarray(curr_series_A)

    # nuclear_prediction = estB.predict(curr_input_B)
    # print "nuclear_prediction:", nuclear_prediction


    return hydro_prediction





def predict_using_mo_data(curr_solar,curr_wind,hydro_prediction,curr_demand):
    #### PREDICTING COAL ###
    solar_mo_series = query_EIA_fuel_monthly_Series('solar')
    wind_mo_series = query_EIA_fuel_monthly_Series('wind')
    nuclear_mo_series = query_EIA_fuel_monthly_Series('nuclear')
    hydro_mo_series = query_EIA_fuel_monthly_Series('hydro')
    coal_mo_series = query_EIA_fuel_monthly_Series('coal')
    gas_mo_series = query_EIA_fuel_monthly_Series('gas')
    other_mo_series = query_EIA_fuel_monthly_Series('other')
        # not including gas, as it is the resource which changes the most through a given day.
        # therefore, when we breakdown the total fuel mix as a part of the total demand....we'll leave gas as the remainder serving the load until the peak daily curve.  Fits reality.

     #########################################
    # using x1,x2,x3,x4 = solar, wind, nuclear, hydro. y=coal.

    # combine series into table with column headers = x vars
    x_vars_dict = {'solar': solar_mo_series,
                    'wind': wind_mo_series,
                    'hydro': hydro_mo_series
                    }

    df_x_vars = DataFrame(x_vars_dict)
    # print df_x_vars
     #########################################

    #### PREDICTING GAS #####

    # get series with y values
    series_y_var = gas_mo_series

    Y = np.asarray(series_y_var)
    X = np.asarray(df_x_vars)

    print "PREDICTING GAS"
    print "shape X", X.shape
    print "shape y", Y.shape

    print "est.fit(X, Y)", est1.fit(X,Y)
    print "est.coef_", est1.coef_

    curr_dict = {'solar':curr_solar, 'wind':curr_wind, 'hydro':hydro_prediction}
    curr_series = Series(curr_dict)
    curr_input = np.asarray(curr_series)

    gas_prediction = est1.predict(curr_input)
    print "gas_prediction:", gas_prediction



    # #### PREDICTING HYDRO #####

    # # update using predicted values
    # x_vars_dict_2 = {'solar': solar_mo_series,
    #                 'wind': wind_mo_series,
    #                 'gas': gas_mo_series
    #                 }

    # df_x_vars_2 = DataFrame(x_vars_dict_2)

    # # get series with y values
    # series_y_var_2 = hydro_mo_series

    # Y2 = np.asarray(series_y_var_2)
    # X2 = np.asarray(df_x_vars_2)

    # print "PREDICTING HYDRO"
    # print "shape X", X2.shape
    # print "shape y", Y2.shape

    # print "est.fit(X, Y)", est2.fit(X2,Y2)
    # print "est.coef_", est2.coef_

    # curr_dict_2 = {'solar':curr_solar, 'wind':curr_wind, 'gas':gas_prediction}
    # curr_series_2 = Series(curr_dict_2)
    # curr_input_2 = np.asarray(curr_series_2)

    # hydro_prediction = est2.predict(curr_input_2)
    # print "hydro_prediction:", hydro_prediction



    #### PREDICTING NUCLEAR #####

    x_vars_dict_3 = {'solar': solar_mo_series,
                    'wind': wind_mo_series,
                    'hydro': hydro_mo_series,
                    'gas': gas_mo_series
                    }

    df_x_vars_3 = DataFrame(x_vars_dict_3)

    # get series with y values
    series_y_var_3 = nuclear_mo_series

    Y3 = np.asarray(series_y_var_3)
    X3 = np.asarray(df_x_vars_3)

    print "PREDICTING NUCLEAR"
    print "shape X", X3.shape
    print "shape y", Y3.shape

    print "est.fit(X, Y)", est3.fit(X3,Y3)
    print "est.coef_", est3.coef_

    curr_dict_3 = {'solar':curr_solar, 'wind':curr_wind, 'hydro':hydro_prediction, 'gas':gas_prediction}
    curr_series_3 = Series(curr_dict_3)
    curr_input_3 = np.asarray(curr_series_3)

    nuclear_prediction = est3.predict(curr_input_3)
    print "nuclear_prediction:", nuclear_prediction


    #### PREDICTING OTHER #####

    x_vars_dict_4 = {'solar': solar_mo_series,
                    'wind': wind_mo_series,
                    'nuclear': nuclear_mo_series,
                    'gas': gas_mo_series,
                    'hydro': hydro_mo_series
                    }

    df_x_vars_4 = DataFrame(x_vars_dict_4)

    # get series with y values
    series_y_var_4 = other_mo_series

    Y4 = np.asarray(series_y_var_4)
    X4 = np.asarray(df_x_vars_4)

    print "PREDICTING OTHER"
    print "shape X", X4.shape
    print "shape y", Y4.shape

    print "est.fit(X, Y)", est4.fit(X4,Y4)
    print "est.coef_", est4.coef_

    curr_dict_4 = {'solar':curr_solar, 'wind':curr_wind, 'nuclear':nuclear_prediction, 'gas':gas_prediction, 'hydro':hydro_prediction}
    curr_series_4 = Series(curr_dict_4)
    curr_input_4 = np.asarray(curr_series_4)

    other_prediction = est4.predict(curr_input_4)
    print "other_prediction:", other_prediction


    #### PREDICTING COAL #####
    # get series with y values
    series_y_var_5 = other_mo_series

    Y5 = np.asarray(series_y_var_5)
    X4 = np.asarray(df_x_vars_4)

    print "PREDICTING COAL"
    print "shape X", X4.shape
    print "shape y", Y5.shape

    print "est.fit(X, Y)", est5.fit(X4,Y5)
    print "est.coef_", est5.coef_

    coal_prediction = est5.predict(curr_input_4)
    print "coal_prediction:", coal_prediction


    #### STANDARDIZE RESULT #####

    remaining = curr_demand - (curr_solar + curr_wind + hydro_prediction)
    scaler =  remaining / (gas_prediction + coal_prediction + nuclear_prediction + other_prediction)

    gas_prediction, coal_prediction, nuclear_prediction, other_prediction = gas_prediction*scaler, coal_prediction*scaler, nuclear_prediction*scaler, other_prediction*scaler


    return gas_prediction, coal_prediction, nuclear_prediction, other_prediction





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
    predict_current_mix(5200,800,24000)       # solar, wind, demand # hr 13-14
    # predict_current_mix(0,2078,20000)       # solar, wind, demand.  # hr 6




