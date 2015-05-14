from pandas import DataFrame
import unicodedata


# when launching server.py, this statement prints to confirm is connected
test = "pandas is connected"


##########################################################################

"""These calculations are used for 1 of 3 purposes:

    (1) PER COUNTY (in California) -- to create the starting counts of fuel percentages for the topojson map on the frontend.

    (2) PER STATE (in USA) -- to create the starting counts of fuel percentages for the topojson map on the frontend.

    (3) to provide data to for the prediction of current fuel usage

The first three functions below, are for these purposes.  And call to other functions, as needed, to perform specific tasks."""

##########################################################################

# get county data for 1 state, as chosen by the user
def fuel_mix_for_map(for_state):
    # retrieve raw data from persistent database
    df2013, df2014, dict_counties = retrieve_from_db(for_state)

    # process data into a single, nested dict.  listing all 12 months (per fuel, per county)
    fuel_mix_12mo = assign_county_and_agg(dict_counties, fuel_codes, df2014, df2013)

    # sum annually,
    annual_mix = sum_annual(fuel_mix_12mo)

    #  then convert to percentages, for frontend data map
    fuel_mix_for_map = annual_percentages(annual_mix)

    # return to the flask route calling this py file.
    return fuel_mix_for_map



# all of the usa, per state
def fuel_mix_for_map_usa():
    # retrieve raw data from persistent database
    df2013_states, df2014_states = retrieve_from_db_usa()

    # process data into a single, nested dict.  listing all 12 months (per fuel, per state)
    fuel_mix_12mo = agg_by_state(fuel_codes, df2014_states, df2013_states)

    # sum annually,
    annual_mix = sum_annual(fuel_mix_12mo)

    #  then convert to percentages, for frontend data map
    fuel_mix_for_map = annual_percentages(annual_mix)

    # return to the flask route calling this py file.
    return fuel_mix_for_map






###########################################################################
##########################################################################
# FUNCTIONS SPECIFIC FOR COUNTY MAP

def retrieve_from_db(state_code):
    """imports model, pulls mwh production data from db, and places into pandas df.
    Also pulls county for each plant_name, and places into dict."""

    # add parent directory to the path, so can import model.py
    #  need model in order to update the database when this task is activated by cron
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

    import model
    s = model.connect()

    # retrive DECEMBER production data, for all turbines at all power plants in California
    CA_gen_dec13_obj = s.execute('SELECT plant_name, state, fuel_type, dec_mwh_gen FROM "ProdGensDec2013" WHERE state=\'%s\' ' % state_code)

    CA_gen_dec13_data = CA_gen_dec13_obj.fetchall()
    df_dec2013 = DataFrame(CA_gen_dec13_data)
    df_dec2013.columns = ['plant_name', 'state', 'fuel_type', 'dec_mwh_gen']

    # retrive JAN-NOV 2014 production data, for all turbines at all power plants in California
    CA_gen_2014_obj = s.execute('SELECT plant_name, state, fuel_type, jan_mwh_gen, feb_mwh_gen, mar_mwh_gen, apr_mwh_gen, may_mwh_gen, jun_mwh_gen, jul_mwh_gen, aug_mwh_gen, sep_mwh_gen, oct_mwh_gen, nov_mwh_gen FROM "ProdGens" WHERE state=\'%s\' ' % state_code)

    CA_gen_2014_data = CA_gen_2014_obj.fetchall()
    df_2014 = DataFrame(CA_gen_2014_data)
    df_2014.columns = ['plant_name', 'state', 'fuel_type', 'jan_mwh_gen', 'feb_mwh_gen', 'mar_mwh_gen', 'apr_mwh_gen', 'may_mwh_gen', 'jun_mwh_gen', 'jul_mwh_gen', 'aug_mwh_gen', 'sep_mwh_gen', 'oct_mwh_gen', 'nov_mwh_gen']

    # retrieve county name, assigned to each turbine at each plant in California
    CA_counties_obj = s.execute('SELECT plant_name, county FROM "StatsGens" WHERE state=\'%s\' GROUP BY plant_name' % state_code)

    CA_plant_counties = CA_counties_obj.fetchall()
    df_counties = DataFrame(CA_plant_counties)
    df_counties.columns = ['plant_name', 'county']
    # now convert into dict, so caan easily add county to other df.
    dict_counties={}
    for idx, row in enumerate(df_counties.values):
        plant_name, county = row
        # clean the county name
        county = unicodedata.normalize('NFKD', county).encode('ascii', 'ignore')
        county = county.lower().title()
        county = county.replace(" County", "")
        dict_counties[plant_name] = county


    return df_dec2013, df_2014, dict_counties





def assign_county_and_agg(dict_counties, fuel_codes, df_jan_to_nov, df_dec):
    """takes all 12 months of data, spread across two df's, and combines.
    places into more mutable nested dict structure.
    assigns, and aggregates, by county (using plant_name/county dict)."""

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
            county = dict_counties[plant_name]


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





###########################################################################
##########################################################################
# FUNCTIONS SPECIFIC FOR USA (STATES)


def retrieve_from_db_usa():
    """imports model, pulls mwh production data from db, and places into pandas df.
    Also pulls state for each plant_name, and places into dict."""

    # add parent directory to the path, so can import model.py
    #  need model in order to update the database when this task is activated by cron
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir)

    import model
    s = model.connect()

    # retrive DECEMBER production data, for all turbines at all power plants in California
    USA_gen_dec13_obj = s.execute('SELECT plant_name, state, fuel_type, dec_mwh_gen FROM "ProdGensDec2013" ')
    USA_gen_dec13_data = USA_gen_dec13_obj.fetchall()
    df_dec2013 = DataFrame(USA_gen_dec13_data)
    df_dec2013.columns = ['plant_name', 'state', 'fuel_type', 'dec_mwh_gen']

    # retrive JAN-NOV 2014 production data, for all turbines at all power plants in USA
    USA_gen_2014_obj = s.execute('SELECT plant_name, state, fuel_type, jan_mwh_gen, feb_mwh_gen, mar_mwh_gen, apr_mwh_gen, may_mwh_gen, jun_mwh_gen, jul_mwh_gen, aug_mwh_gen, sep_mwh_gen, oct_mwh_gen, nov_mwh_gen FROM "ProdGens" ')
    USA_gen_2014_data = USA_gen_2014_obj.fetchall()
    df_2014 = DataFrame(USA_gen_2014_data)
    df_2014.columns = ['plant_name', 'state', 'fuel_type', 'jan_mwh_gen', 'feb_mwh_gen', 'mar_mwh_gen', 'apr_mwh_gen', 'may_mwh_gen', 'jun_mwh_gen', 'jul_mwh_gen', 'aug_mwh_gen', 'sep_mwh_gen', 'oct_mwh_gen', 'nov_mwh_gen']

    return df_dec2013, df_2014





def agg_by_state(fuel_codes, df_jan_to_nov, df_dec):
    """takes all 12 months of data, spread across two df's, and combines.
    places into more mutable nested dict structure.
    assigns, and aggregates, by county (using plant_name/county dict)."""

    # output of function  = makes dictionary of states
    fuel_per_state = { }

    #  note -- the retrieved row in only a copy, not the original. Dataframes are good for data manipulation (e.g. pivot table), but are not very mutable.
    for idx,row in enumerate(df_jan_to_nov.values):

        # get all the data, and insert into nested dict
        plant_name, state, fuel_type, mwh_gen = row[0], row[1], row[2], row[3:]
        # convert fuel code, to actual fuel name
        fuel_type_name = fuel_codes[fuel_type]

        starting_totals = [0,0,0,0,0,0,0,0,0,0,0,0]

        # only add to dict, if not "State Incremental Fuel Level":
        if plant_name != "State-Fuel Level Increment":

            # add to dict, summing the list per month:
            if state not in fuel_per_state:
                fuel_per_state[state] = {
                "gas":starting_totals,
                "coal":starting_totals,
                "solar":starting_totals,
                "wind":starting_totals,
                "nuclear": starting_totals,
                "hydro":starting_totals,
                "other":starting_totals
                }

            already_in_dict = fuel_per_state[state][fuel_type_name]
            replace_in_dict = [ (mwh_gen[i]+int(already_in_dict[i]) ) for i in range(len(mwh_gen)) ]

            fuel_per_state[state][fuel_type_name] = replace_in_dict

    # add the december fuel data. make sure to add the 12th month
    for idx,row in enumerate(df_dec.values):
        plant_name = row[0]     # for each row, get the plant name

        # make sure we know the state, before we take the data
        if plant_name != "State-Fuel Level Increment":

        # get all the data, and insert into nested dict
            plant_name, state, fuel_type, mwh_gen = row[0], row[1], row[2], row[3:]
            # convert fuel code, to actual fuel name
            fuel_type_name = fuel_codes[fuel_type]

            # add to dict, as the 12th month in the list:
            in_dict = fuel_per_state[state][fuel_type_name]
            if len(in_dict) < 12:
                in_dict.append(int(mwh_gen))
            else:
                in_dict[11] += int(mwh_gen)
            fuel_per_state[state][fuel_type_name] = in_dict

    return fuel_per_state




###########################################################################
##########################################################################
# NOT SPECIFIC FUNCTIONS.  Used for counties and states.


def sum_annual(nested_dict):
    """takes nested dict {county/state:{fuel: [jan,feb,...]} }, and adds up annual usage."""

    annual_fuel_mix = {}
    # look at the mix per county/state.  {fuel: [jan,feb,...], fuel: ...}
    for geo_pt, fuel_mix in nested_dict.items():
        add_to_dict = {}
        # look at each fuel, in the mix.  fuel: [jan,feb,...].  per month
        for fuel_type, per_mo in fuel_mix.items():
            annual_sum = 0
            for i in range(len(per_mo)):
                mwh = per_mo[i]
                annual_sum += mwh
            add_to_dict[fuel_type] = annual_sum
        annual_fuel_mix[geo_pt] = add_to_dict

    return annual_fuel_mix




def annual_percentages(nested_dict):
    """takes nested dict of annual mwh gen,
        {county/state:{fuel:int, fuel:int, ...}, county/state:...},
         and converts to a percentage per each fuel type"""

    #new output dict
    dict_with_percentage = {}

    # look at the mix per county/state.  {fuel:...,fuel:...}
    for geo_pt, fuel_mix in nested_dict.items():
        dict_with_percentage[geo_pt] = {
            "gas":0,
            "coal":0,
            "solar":0,
            "wind":0,
            "nuclear": 0,
            "hydro":0,
            "other":0
            }
        sum_mwh = 0
        # get sum of mwh across fuels
        for fuel,mwh in fuel_mix.items():
            sum_mwh += mwh
        # convert to ratios, enter into new dict
        for fuel,mwh in fuel_mix.items():
            if mwh != 0:
                percent_as_num = (mwh/sum_mwh)*100
                dict_with_percentage[geo_pt][fuel] = round(percent_as_num,0)

    return dict_with_percentage





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
    "WH":'other',
    "SC": 'coal',    # syncoal (low ash)
    "OTH":'gas',     # other gases
    "PUR": 'other',  # I could not identify
    "SGP": 'other',     # I coudl not identify
    "MWH": 'other'      # bad data entry
}



if __name__ == "__main__":
    fuel_mix_for_map()



