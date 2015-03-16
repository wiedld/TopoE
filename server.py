from flask import Flask, render_template, redirect, request, jsonify
import model
import os

##  these are used within functions.
# on server startup, the messages print to confirm flask can find
from calculations import pandas_data_munging as pdm
print pdm.test
from calculations import binary_decision_tree as bdt
print bdt.test


## this is used outside of a function
from tasks import CAISO_flask_data_scraper as RT_scrape
print RT_scrape.test
from tasks import CAISO_flask_api as RT_api
print RT_api.test
from tasks import ML_linear_regression_v2 as ML
print ML.test



app = Flask(__name__)
app.secret_key = os.environ["flask_app_key"]



# HOMEPAGE
@app.route("/")
def index():
    """Initial rendering when begin on page"""
    return render_template("index.html")


#########################################################
#########################################################
# STATE MAP -- CLICK ON COUNTIES


@app.route("/county_map")
def county_map():
    """rendering the county-map. has js file with insertion of interactive d3 elements (slider, donut)."""

    return render_template("county_map.html")




@app.route("/county-map-data", methods=['POST'])
def county_map_data():
    """get data for topojson map of counties.  Called during initial rendering."""
    chosen_state = request.data
    # print "CHOSEN STATE:", chosen_state

    data_for_topojson = pdm.fuel_mix_for_map(chosen_state)
    # print "DATA FOR MAP: \n", data_for_topojson
    return jsonify(data_for_topojson)




@app.route("/scenario-result", methods=['POST'])
def scenario_result():
    """Take data structure from frontend, pipe through binary_decision_tree, return result to front."""

    from calculations import binary_decision_tree as bdt
    print bdt.test

    user_input = request.json
    result = bdt.bdt_on_user_input(user_input)

    return jsonify(result)


#########################################################
#########################################################
# USA MAP -- CLICK ON STATES

@app.route("/usa_map")
def usa_map():
    """rendering the usa-map. has js file with insertion of interactive d3 elements (slider, donut)."""

    return render_template("usa_map.html")




@app.route("/usa-map-data", methods=['POST'])
def usa_map_data():
    """get data for topojson map of counties.  Called during initial rendering."""

    data_for_topojson = pdm.fuel_mix_for_map_usa()
    return jsonify(data_for_topojson)




@app.route("/scenario-result-usa", methods=['POST'])
def scenario_result_usa():
    """Take data structure from frontend, pipe through binary_decision_tree, return result to front."""

    from calculations import binary_decision_tree as bdt
    print bdt.test

    user_input = request.json
    result = bdt.bdt_on_user_input_usa(user_input)

    return jsonify(result)



#########################################################
#########################################################
#  CURRENT MIX

# default to use:
predicted_curr_mix = {'nuclear': 1094.0, 'gas': 12314.0, 'coal': 1795.0, 'other': 1795.0, 'solar': 3678.0, 'wind': 272.0, 'hydro': 1457.0}
# default is updated by the "While True" function at the end of this server, which queries CAISO and updates every 10 minutes.


@app.route("/current")
# def current_mix(mix=predicted_curr_mix):
def current_mix():

    return render_template("current_mix.html")


@app.route("/current-mix-data", methods=['POST'])
def current_mix_data():
    """Take data structure for current fuel mix, and pipe through to frontend object"""

    solar, wind = RT_scrape.get_solar_wind()
    print "solar:", solar
    print "wind:", wind

    demand = 22000
    # call to CAISO_flask_api for recent demand

    predicted_curr_mix = ML.predict_current_mix(solar,wind,demand)

    print predicted_curr_mix

    now_data = {'nuclear': 1328.0, 'gas': 14937.0, 'coal': 2180.0, 'other': 2180.0, 'solar': 0.0, 'wind': 614.0, 'hydro': 760.0}

    return jsonify(now_data)




###########################################################
###########################################################
# ABOUT

@app.route("/about")
def about_HB_project():
    """Explains how the under-the-cover works."""

    return render_template("about.html")



#########################################################
#########################################################



def main():
    """For future use."""
    pass


if __name__ == "__main__":
    main()
    # app.run(host="0.0.0.0", debug=False)
    app.run(debug=True)



#########################################################
#########################################################


"""Countinously updates the global variable predicted_curr_mix while server is running.  At end of flask route, so everything above is executed first when server is launched."""

# while True:
#     solar, wind = RT_scrape.get_solar_wind()
#     print "solar:", solar
#     print "wind:", wind

#     demand = 22000
#     # call to CAISO_flask_api for recent demand

#     predicted_curr_mix = ML.predict_current_mix(solar,wind,demand)


