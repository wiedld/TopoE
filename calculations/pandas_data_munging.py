from pandas import DataFrame, merge


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

    CA_gen_dec13 = s.execute('SELECT plant_name, state, fuel_type, dec_mwh_gen FROM ProdGensDec2013 WHERE state="CA" ')
    CA_gen_dec13_data = CA_gen_dec13.fetchall()
    df_dec2013 = DataFrame(CA_gen_dec13_data)
    df_dec2013.columns = ['plant_name', 'state', 'fuel_type', 'dec_mwh_gen']

    CA_gen_2014 = s.execute('SELECT plant_name, state, fuel_type, jan_mwh_gen, feb_mwh_gen, mar_mwh_gen, apr_mwh_gen, may_mwh_gen, jun_mwh_gen, jul_mwh_gen, aug_mwh_gen, sep_mwh_gen, oct_mwh_gen, nov_mwh_gen FROM ProdGens WHERE state="CA" ')
    CA_gen_2014_data = CA_gen_2014.fetchall()
    df_2014 = DataFrame(CA_gen_2014_data)
    df_2014.columns = ['plant_name', 'state', 'fuel_type', 'jan_mwh_gen', 'feb_mwh_gen', 'mar_mwh_gen', 'apr_mwh_gen', 'may_mwh_gen', 'jun_mwh_gen', 'jul_mwh_gen', 'aug_mwh_gen', 'sep_mwh_gen', 'oct_mwh_gen', 'nov_mwh_gen']

    ##############################################
    # THIS SECTION IS FOR TROUBLESHOOTING!  Is all working at the moment.

    # print df_dec2013
    # print df_2014

    # dec_plants = df_dec2013['plant_name'].value_counts()
    # plants = df_2014['plant_name'].value_counts()
    # print dec_plants
    # print plants


    # by_fuel_plant_dec = df_dec2013.groupby(['plant_name', 'fuel_type'])
    # # agg_counts_dec = by_fuel_plant_dec.sum()
    # # print agg_counts_dec

    # by_fuel_plant_2014 = df_2014.groupby(['plant_name', 'fuel_type'])
    # agg_counts_2014 = by_fuel_plant_2014.sum()
    # print agg_counts_2014

    ##############################################

    # TODO:  make sure to ignore (remove) for plant_name ="State-Fuel Level Increment"

    ##############################################

    #  TODO:  get the two fuels to merge/join together
        ## these below methods failed.
    # by_fuel_plant = by_fuel_plant_2014.join(by_fuel_plant_dec, on="plant_name", how='left', lsuffix="_review")
    # by_fuel_plant_2014.join(by_fuel_plant_dec, on='plant_name', how='left', lsuffix="_review")
    # by_fuel_plant = merge(by_fuel_plant_2014, by_fuel_plant_dec, on="plant_name", how='outer')

        ##  this method succeeded, however, there was zero overlap on the plant_name.
    df_all_months = df_2014.join(df_dec2013, on='plant_name', how='inner', lsuffix="_review")
    print df_all_months
    by_fuel_plant = df_all_months.groupby(['plant_name', 'fuel_type'])

    agg_counts = by_fuel_plant.sum()
    print agg_counts

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
    retrieve_from_db()


