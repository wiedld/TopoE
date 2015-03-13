from flask import Flask, render_template, redirect, request, jsonify
import model
import os

from calculations import pandas_data_munging as pdm
print pdm.test

# from calculations import binary_decision_tree as bdt
# print bdt.test



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

@app.route("/current")
def current_mix():
    """Take data structure for current fuel mix, and pipe through to frontend object"""

    return render_template("current_mix.html")


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


