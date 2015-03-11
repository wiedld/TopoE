from flask import Flask, render_template, redirect, request, jsonify
import model
import os

from calculations import pandas_data_munging as pdm
print pdm.test

# from calculations import binary_decision_tree as bdt
# print bdt.test



app = Flask(__name__)
app.secret_key = os.environ["flask_app_key"]



@app.route("/")
def index():
    """Initial rendering when begin on page"""

    return render_template("index.html")



@app.route("/county-map", methods=['POST'])
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
# TRYING OUT ANOTHER MAP

@app.route("/usa")
def index2():
    """Initial rendering when begin on page"""
    return render_template("index2.html")


@app.route("/usa-map", methods=['POST'])
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



###########################################################
###########################################################



def main():
    """For future use."""
    pass


if __name__ == "__main__":
    main()
    # app.run(host="0.0.0.0", debug=False)
    app.run(debug=True)


