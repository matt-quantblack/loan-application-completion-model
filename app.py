from flask import Flask, render_template, jsonify, request
from google_analytics.ga_adapter import GAAdapter
from utils.upload_utils import validate_upload_file
import os

GA_CRED_PATH = './google_analytics_cred.json'

app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template("dashboard.html")


# A route to check if google analytics credentials are setup.
@app.route('/api/v1/ga/cred_check', methods=['GET'])
def api_cred_check():
    exists = os.path.isfile(GA_CRED_PATH)
    return jsonify({'success', exists})


# A route to overwrite or add the google analytics credentials.
@app.route('/api/v1/ga/cred_set', methods=['POST'])
def api_cred_set():

    # Validate the file is acceptable
    file, error = validate_upload_file(request.files, extensions=["json"])

    # Save the file to the google_analytics_cred.json
    if file:
        file.save(GA_CRED_PATH)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': error})


# A route to return all of the available profiles in a google account.
@app.route('/api/v1/ga/profiles/all', methods=['GET'])
def api_all_profiles():
    ga_adapter = GAAdapter()
    ga_adapter.connect(scopes=['https://www.googleapis.com/auth/analytics.readonly'],
                       key_file_location=GA_CRED_PATH)
    profiles = ga_adapter.get_profiles()

    return jsonify({'success': True, 'data': profiles})


if __name__ == '__main__':
    app.run()
