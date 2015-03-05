from flask import Flask, render_template, redirect, request, session
import model
import os

from calculations import pandas_data_munging as pdm
print pdm.test

from calculations import binary_decision_tree as bdt
print bdt.test



app = Flask(__name__)
app.secret_key = os.environ["flask_app_key"]



@app.route("/")
def index():
    """Initial rendering when begin on page"""
    return render_template("index.html")


@app.route("/zip-county-zone")
def zip_county_zone():
    """translate the user input zip code into: county, and the CAISO load zone.  Save all three values in session for user."""
    pass

@app.route("/fuel-type-county-map")
def fuel_type_county_map():
    """using the db data, display a map with the fuel type per county.  Use EIA 923 data.  display format TBD."""
    pass



###########################################################
##  these routes are temporary.  For viewing different d3 options, which may be used later.


@app.route("/donut")
def donuts():
    return render_template("donuts.html")


###########################################################



def main():
    """For future use."""
    pass

if __name__ == "__main__":
    main()
    app.run(debug=True)