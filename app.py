from threading import Timer

from flask import Flask, render_template, jsonify, request, send_file
from application.ga_adapter import get_profiles
from utils.upload_utils import validate_upload_file
from flask import send_from_directory
from application import file_manager
from application import model_builder
import webbrowser
import os
import json


GA_CRED_PATH = 'google_analytics_cred.json'
DATA_TEMPLATE_PATH = 'data_template.csv'

app = Flask(__name__)

# A route to add the program icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# A route to server the default dashboard template
@app.route('/')
def dashboard():
    return render_template("dashboard.html")


# A route to check if google analytics credentials are setup.
@app.route('/api/v1/ga/check_cred', methods=['GET'])
def api_check_cred():
    try:
        exists = file_manager.file_exists(GA_CRED_PATH)
        return jsonify({'success': True, 'result': exists})
    except IOError:
        return jsonify({'success': False, 'error': 'IO Error could not delete credentials file'})


# A route to overwrite or add the google analytics credentials.
@app.route('/api/v1/ga/cred_set', methods=['POST'])
def api_cred_set():

    # Validate the file is of correct type
    file, error = validate_upload_file(request.files, extensions=["json"])

    # Save the file to the google_analytics_cred.json
    if file:
        file_manager.update_ga_credentials_file(file, GA_CRED_PATH)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': error})


# A route to remove google analytics credentials.
@app.route('/api/v1/ga/cred_remove', methods=['GET'])
def api_cred_remove():

    # Remove the google_analytics_cred.json
    try:
        file_manager.remove_ga_credentials_file(GA_CRED_PATH)
        return jsonify({'success': True})
    except FileNotFoundError:
        return jsonify({'success': False, 'error': 'File doesn\'t exit.'})
    except IOError:
        return jsonify({'success': False, 'error': 'IO Error could not delete credentials file'})


# A route to return all of the available profiles in a google account.
@app.route('/api/v1/ga/profiles/all', methods=['GET'])
def api_all_profiles():

    try:
        profiles = get_profiles(GA_CRED_PATH)
    except ValueError as err:
        return jsonify({'success': False, 'error': 'Cant connect to Google Analytics: {}'.format(err)})

    return jsonify({'success': True, 'data': profiles})


# A route to check local storage for data descriptors for the provided field names
# used to pre fill the datatype for each field in the selected data csv on client side
@app.route('/api/v1/data_template/details', methods=['POST'])
def api_data_template_details():

    # extract the required field names from the get request - so we only send back details of these fields
    field_names = request.form.getlist("data[]")

    # Hack to remove \r character from last entry of list
    field_names = [name.strip() for name in field_names]

    # Get the field details from the data template
    rows = file_manager.csv_to_list(DATA_TEMPLATE_PATH)

    # Only include the required field names
    details = [row for row in rows if row[0] in field_names]

    # Return the response
    if details is not None:
        return jsonify({'success': True, 'data': details})
    else:
        return jsonify({'success': False})

# The route to upload the csv data, build the ML models and return a priority list of customers
# for follow up phone calls.
@app.route('/api/v1/model/build', methods=['POST'])
def api_model_build():

    # Validate the file is acceptable
    file, error = validate_upload_file(request.files, extensions=["csv"])

    # Get the Google Analytics profile id if selected
    ga_profile_id = request.form.get("connect_ga")

    # Get the list of fields and the data type descriptors
    fields_string = request.form.get("fields")

    # Load the fields into a object from a json string
    fields = json.loads(fields_string)

    # Get a dataframe of the contacts as a Pandas Dataframe ranked by the probability
    # of completing application.
    # This is the main guts of application, parses data, builds model and makes predictions
    try:
        contacts = model_builder.build_and_predict(file, DATA_TEMPLATE_PATH, fields, ga_profile_id, GA_CRED_PATH)
    except ValueError as err:
        return jsonify({'success': False, 'error': str(err)})

    # Jsonify the data from a Panads Dataframe to a string
    json_str = contacts.to_json(orient="records")

    # Convert back to a json object and add success = true
    json_data = {
        'data': json.loads(json_str),
        'success': True
    }

    # Jsonify the response
    return jsonify(json_data)


# A route to export the data to an excel file
@app.route('/api/v1/model/export_to_excel', methods=['POST'])
def export_to_excel():

    # Data is sent in the post
    if "data" in request.form:
        customers_string = request.form.get("data")

        # Build into a list from the json string
        customers = json.loads(customers_string)

        # Create an excel file stream from the data
        file = model_builder.export_to_excel(customers)

        # construct response and attach the excel file stream
        response = send_file(
            file,
            as_attachment=True,
            attachment_filename='customerList.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # Return the response which will be a file download
        return response
    else:
        return jsonify({'success': False, 'error': 'The data did not exist in the POST request'})


# Loads the default webbrowser to activate the GUI for the application
def open_browser():
    webbrowser.open('http://localhost:5000/')


# Start the flask application
if __name__ == '__main__':
    # Start a timer that will load the webbrowser in a new thread after flask app has
    # started
    Timer(1, open_browser).start()
    app.run()


