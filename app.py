from flask import Flask, render_template, jsonify, request, Response
from application.ga_adapter import get_profiles
from utils.upload_utils import validate_upload_file
from flask import send_from_directory
from application import file_manager
from application import model_builder
import os
import json

GA_CRED_PATH = 'google_analytics_cred.json'
DATA_TEMPLATE_PATH = 'data_template.csv'

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def dashboard():
    return render_template("dashboard.html")


# A route to check if google analytics credentials are setup.
@app.route('/api/v1/ga/check_cred', methods=['GET'])
def api_check_cred():
    exists = file_manager.file_exists(GA_CRED_PATH)
    return jsonify({'success': exists})


# A route to overwrite or add the google analytics credentials.
@app.route('/api/v1/ga/cred_set', methods=['POST'])
def api_cred_set():

    # Validate the file is acceptable
    file, error = validate_upload_file(request.files, extensions=["json"])

    # Save the file to the google_analytics_cred.json
    if file:
        file_manager.update_ga_credentials_file(file, GA_CRED_PATH)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': error})


# A route to return all of the available profiles in a google account.
@app.route('/api/v1/ga/profiles/all', methods=['GET'])
def api_all_profiles():

    profiles = get_profiles(GA_CRED_PATH)

    return jsonify({'success': True, 'data': profiles})


@app.route('/api/v1/data_template/details', methods=['POST'])
def api_data_template_details():
    """ A route to check local storage for data descriptors for the provided field names
    used to pre fill the datatype for each field in the selected data csv on client side
    """

    #extract the required field names from the get request - so we only send back details of these fields
    field_names = request.form.getlist("data[]")

    #get the field details from the data template
    rows = file_manager.csv_to_list(DATA_TEMPLATE_PATH)

    #only include the required field names
    details = [row for row in rows if row[0] in field_names]

    #return the respnonse
    if details is not None:
        return jsonify({'success': True, 'data': details})
    else:
        return jsonify({'success': False})

@app.route('/api/v1/model/build', methods=['POST'])
def api_model_build():
    """ The route to upload the csv data, build the ML models and return a priority list of customers
    for follow up calls.
    """

    # Validate the file is acceptable
    file, error = validate_upload_file(request.files, extensions=["csv"])

    connect_ga = request.form.get("connect_ga")
    fields_string = request.form.get("fields")
    fields = json.loads(fields_string)

    #get a dataframe of the contacts as a Pandas Dataframe
    contacts = model_builder.build_and_predict(file, DATA_TEMPLATE_PATH, fields, connect_ga)

    #jsonify the data from a Panads Dataframe
    json_data = contacts.to_json(orient="records")
    return Response(json_data, mimetype='application/json')


if __name__ == '__main__':
    app.run()
