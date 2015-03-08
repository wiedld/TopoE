from pandas import DataFrame


# when launching server.py, this statement prints to confirm is connected
test = "pandas is connected"




def retrieve_from_db():
    """imports model, pulls mwh production data from db, and places into pandas df.  Merges together for 12 annual months, and includes county for each plant_name."""

    # add parent directory to the path, so can import model.py
    #  need model in order to update the database when this task is activated by cron
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)
    import model
    s = model.connect()

    # retrive DECEMBER production data, for all turbines at all power plants in California
    CA_gen_dec13_obj = s.execute('SELECT plant_name, operator_name, state, fuel_type, dec_mwh_gen FROM ProdGensDec2013 WHERE state="CA" ')
    CA_gen_dec13_data = CA_gen_dec13_obj.fetchall()
    df_dec2013 = DataFrame(CA_gen_dec13_data)
    df_dec2013.columns = ['plant_name', 'operator_name', 'state', 'fuel_type', 'dec_mwh_gen']

    # retrive JAN-NOV 2014 production data, for all turbines at all power plants in California
    CA_gen_2014_obj = s.execute('SELECT plant_name, operator_name, state, fuel_type, jan_mwh_gen, feb_mwh_gen, mar_mwh_gen, apr_mwh_gen, may_mwh_gen, jun_mwh_gen, jul_mwh_gen, aug_mwh_gen, sep_mwh_gen, oct_mwh_gen, nov_mwh_gen FROM ProdGens WHERE state="CA" ')
    CA_gen_2014_data = CA_gen_2014_obj.fetchall()
    df_2014 = DataFrame(CA_gen_2014_data)
    df_2014.columns = ['plant_name', 'operator_name', 'state', 'fuel_type', 'jan_mwh_gen', 'feb_mwh_gen', 'mar_mwh_gen', 'apr_mwh_gen', 'may_mwh_gen', 'jun_mwh_gen', 'jul_mwh_gen', 'aug_mwh_gen', 'sep_mwh_gen', 'oct_mwh_gen', 'nov_mwh_gen']

    # retrieve county name, assigned to each turbine at each plant in Californis
    CA_counties_obj = s.execute('SELECT plant_name, state, county FROM StatsGens WHERE state="CA" GROUP BY plant_name')
    CA_plant_counties = CA_counties_obj.fetchall()
    df_counties = DataFrame(CA_plant_counties)
    df_counties.columns = ['plant_name', 'state', 'county']

    return df_dec2013, df_2014, df_counties




def make_df_byplant_byfuel (df):

    by_fuel_plant = df.groupby(['plant_name', 'operator_name', 'fuel_type'])
    agg_counts = by_fuel_plant.sum()

    return agg_counts




def assign_county_to_plant (df_counties, df_plant_fuel):
    left = df_counties.set_index('plant_name')
    right = df_plant_fuel.set_index('plant_name')

    df_plant_county = left.join(right, lsuffix='_l', rsuffix='_r')
    return df_plant_county





    ##############################################

    # TODO:  make sure to ignore (remove) for plant_name ="State-Fuel Level Increment"

    ##############################################

    ############################################



def counties_into_CAISO():
    """takes panda df, and sorts by counties in each CAISO zone."""

    pass



def sum_annual():
    """takes panda df, and adds up annual usage."""

    pass



def percentage_fuel_type():
    """takes panda df, and makes a percentage per each fuel type"""

    pass




if __name__ == "__main__":
    db2013, db2014, db_counties = retrieve_from_db()

    df_byplant_byfuel_2013 = make_df_byplant_byfuel(db2013)
    df_byplant_byfuel_2014 = make_df_byplant_byfuel(db2014)

    print df_byplant_byfuel_2014 #323
    print df_byplant_byfuel_2013 #292
    print db_counties #934

    aggregated_2013 = assign_county_to_plant(db_counties, df_byplant_byfuel_2013)
    aggregated_2014 = assign_county_to_plant(db_counties, df_byplant_byfuel_2014)

    print aggregated_2013
    print aggregated_2014


