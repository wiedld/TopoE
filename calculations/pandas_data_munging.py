from pandas import DataFrame, Series


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





def assign_county_and_agg(dict_counties, fuel_codes, df_jan_to_nov, df_dec):
    # output of function  = makes dictionary of counties
    fuel_per_county = { }
    for county in dict_counties.values():
        starting_totals = [0,0,0,0,0,0,0,0,0,0,0,0]
        fuel_per_county[county] = {
            "gas":starting_totals,
            "coal":starting_totals,
            "solar":starting_totals,
            "wind":starting_totals,
            "nuclear": starting_totals,
            "hydro":starting_totals,
            "other":starting_totals
            }

    #  note -- the retrieved row in only a copy, not the original. Dataframes are good for data manipulation (e.g. pivot table), but are not very mutable.
    for idx,row in enumerate(df_jan_to_nov.values):
        plant_name = row[0]     # for each row, get the plant name

        # make sure we know the county, before we take the data
        if plant_name in dict_counties:
            county = dict_counties[plant_name]  # update county, for each plant (each row)

            # get all the data, and insert into nested dict
            plant_name, fuel_type, mwh_gen = row[0], row[2], row[3:]
            # convert fuel code, to actual fuel name
            fuel_type_name = fuel_codes[fuel_type]

            # add to dict, summing the list per month:
            already_in_dict = fuel_per_county[county][fuel_type_name]
            replace_in_dict = [ (mwh_gen[i]+int(already_in_dict[i]) ) for i in range(len(mwh_gen)) ]

            fuel_per_county[county][fuel_type_name] = replace_in_dict

    # add the december fuel data. make sure to add the 12th month
    for idx,row in enumerate(df_dec.values):
        plant_name = row[0]     # for each row, get the plant name

        # make sure we know the county, before we take the data
        if plant_name in dict_counties:
            county = dict_counties[plant_name]  # update county, for each plant (each row)

        # get all the data, and insert into nested dict
            plant_name, fuel_type, mwh_gen = row[0], row[2], row[3:]
            # convert fuel code, to actual fuel name
            fuel_type_name = fuel_codes[fuel_type]

            # add to dict, as the 12th month in the list:
            in_dict = fuel_per_county[county][fuel_type_name]
            if len(in_dict) < 12:
                in_dict.append(int(mwh_gen))
            else:
                in_dict[11] += int(mwh_gen)
            fuel_per_county[county][fuel_type_name] = in_dict

    return fuel_per_county





def counties_into_CAISO():
    """takes panda df, and sorts by counties in each CAISO zone."""

    pass



def sum_annual():
    """takes panda df, and adds up annual usage."""

    pass



def percentage_fuel_type():
    """takes panda df, and makes a percentage per each fuel type"""

    pass



fuel_codes = {
    "BIT":'coal',
    "ANT":'coal',
    "LIG":'coal',
    "SUB":'coal',
    "RC":'coal',
    "WC":'coal',
    "CBL":'coal',
    "DFO":'other',  # technically, fuel oil
    "RFO":'other',  # technically, refined oil
    "JF":'other',   # jet fuel
    "KER":'other',  # kerosene
    "WO":'other',   # waste oil
    "PC":'other',    # pertro coke
    "NG":'gas',
    "BFG":'gas',
    "OG":'gas',
    "PG":'gas',     # propane gas
    "SG":'other',   # syngas from petro
    "SGC":'coal',   # syngas from coal
    "AB":'other',   # agri waste
    "MSW":'other',  # muni waste
    "OBS":'other',  # other solid biomass waste
    "WDS":'other',  # wood waste
    "OBL":'other',  # biomass liquid
    "SLW":'other',  # sludge
    "BLQ":'other',  # black liqour
    "WDL":'other',   # wood waste liquids
    "WAT":'hydro',
    "OBG":'other',
    "GEO":'other',
    "LFG":'other',  # landfill gas...not gas from drilling
    "SUN":'solar',
    "NUC":'nuclear',
    "WND":'wind',
    "TDF":'other',
    "MSB":'other',
    "MSN":'other',
    "WH":'other'
}



if __name__ == "__main__":
    df2013, df2014, dict_counties = retrieve_from_db()

    df2013_by_fuel = df2013.groupby(['fuel_type'])
    agg_counts = df2013_by_fuel.sum()
    print agg_counts

    assign_county_and_agg(dict_counties, fuel_codes, df2014, df2013)




