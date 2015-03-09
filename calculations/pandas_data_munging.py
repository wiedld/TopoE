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
    CA_gen_dec13_obj = s.execute('SELECT plant_name, state, fuel_type, dec_mwh_gen FROM ProdGensDec2013 WHERE state="CA" ')
    CA_gen_dec13_data = CA_gen_dec13_obj.fetchall()
    df_dec2013 = DataFrame(CA_gen_dec13_data)
    df_dec2013.columns = ['plant_name', 'state', 'fuel_type', 'dec_mwh_gen']

    # retrive JAN-NOV 2014 production data, for all turbines at all power plants in California
    CA_gen_2014_obj = s.execute('SELECT plant_name, state, fuel_type, jan_mwh_gen, feb_mwh_gen, mar_mwh_gen, apr_mwh_gen, may_mwh_gen, jun_mwh_gen, jul_mwh_gen, aug_mwh_gen, sep_mwh_gen, oct_mwh_gen, nov_mwh_gen FROM ProdGens WHERE state="CA" ')
    CA_gen_2014_data = CA_gen_2014_obj.fetchall()
    df_2014 = DataFrame(CA_gen_2014_data)
    df_2014.columns = ['plant_name', 'state', 'fuel_type', 'jan_mwh_gen', 'feb_mwh_gen', 'mar_mwh_gen', 'apr_mwh_gen', 'may_mwh_gen', 'jun_mwh_gen', 'jul_mwh_gen', 'aug_mwh_gen', 'sep_mwh_gen', 'oct_mwh_gen', 'nov_mwh_gen']

    # retrieve county name, assigned to each turbine at each plant in Californis
    CA_counties_obj = s.execute('SELECT plant_name, county FROM StatsGens WHERE state="CA" GROUP BY plant_name')
    CA_plant_counties = CA_counties_obj.fetchall()
    df_counties = DataFrame(CA_plant_counties)
    df_counties.columns = ['plant_name', 'county']
    # now convert into dict, so caan easily add county to other df.
    dict_counties={}
    for idx, row in enumerate(df_counties.values):
        plant_name, county = row
        dict_counties[plant_name] = county


    return df_dec2013, df_2014, dict_counties




def assign_county_to_plant (dict_counties, df_plant_fuel):

    # rename "state" column to "county"
    df_plant_fuel.rename(columns={'state':'county'}, inplace=True)

    # make a template for the completed df
    columns = df_plant_fuel.columns
    completed_df = DataFrame(columns=columns)

    # replace state names, with county names retrieved from dict
    #  note -- the retrieved row in only a copy, not the original.
    #  therefore, need to insert the row (a numpy ndarray) to a new dataframe
    for idx,row in enumerate(df_plant_fuel.values):
        plant_name = row[0]
        if plant_name in dict_counties:
            row[1] = dict_counties[plant_name]  # returns county
            print row
            completed_df = completed_df.append(DataFrame(data=row))

    # now filter the new df, to only include plants where we have the county.
    #   meaning, where county != 'CA'
    # completed_df = df_plant_fuel[(df_plant_fuel['county'] != 'CA')]

    print completed_df



# def make_df_byplant_byfuel (df):

#     by_fuel_plant = df.groupby(['plant_name', 'fuel_type'])
#     agg_counts = by_fuel_plant.sum()

#     return agg_counts





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
    df2013, df2014, dict_counties = retrieve_from_db()

    completed_df_2013 = assign_county_to_plant(dict_counties, df2013)
    completed_df_2014 = assign_county_to_plant(dict_counties, df2014)

    print completed_df_2013
    print completed_df_2014


