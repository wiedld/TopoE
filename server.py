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



@app.route("/scenario-result", methods=['POST'])
def scenario_result():
    """Take data structure from frontend, pipe through binary_decision_tree, return result to front."""

    from calculations import binary_decision_tree as bdt
    print bdt.test

    user_input = request.json
    result = bdt.bdt_on_user_input(user_input)

    return jsonify(result)



@app.route("/zip-county-zone")
def zip_county_zone():
    """translate the user input zip code into: county, and the CAISO load zone.  Save all three values in session for user."""
    pass



###########################################################
###########################################################



def main():
    """For future use."""
    pass


if __name__ == "__main__":
    main()
    # app.run(host="0.0.0.0", debug=False)
    app.run(debug=True)


