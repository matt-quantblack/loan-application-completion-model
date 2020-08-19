/*
* API calls
*
* Author: Matthew Bailey
*
* Created: 24/07/2020
*/

/**
 * API call that sets the Google Analytics credentials in the local file system
 */
function set_credentials() {

    //render the page for preparing to upload
    render_credential_upload_state();

    //get the file from the form
    let data = new FormData($("#cred-form").get(0));

    //post the file to backend
    api_request_post_file('/api/v1/ga/cred_set', data, function(data) {
        //manage the response
        manage_response(data, render_set_credential_success, render_set_credential_failed, "#cred-error");
    });

}


/**
 * API call that gets all the google analytics profiles
 */
function get_ga_profiles() {

    //make the get request
    $.get("/api/v1/ga/profiles/all", function( data ) {
        //manage the response
        manage_response(data, render_get_ga_profiles_success, render_get_ga_profiles_failed, "#cred-error");
    });
}


/**
 * API call that checks if a Google Analytics credential file is in local storage
 */
function check_credentials()
{
    $.get("/api/v1/ga/check_cred", function( data ) {
        //manage the response
        manage_response(data, render_check_credentials_success, render_check_credentials_failed, "#cred-error");
    });
}


/**
 * API call that removes the google analytics credential file from local storage
 */
function remove_credentials()
{
    $.get("/api/v1/ga/cred_remove", function( data ) {
        //manage the response
        manage_response(data, render_credential_remove_success, null, "#cred-error");
    });
}


/**
 * API call that gets the data types from the supplied field names
 */
function get_data_template(fields)
{
    api_request_post("/api/v1/data_template/details", {'data': fields}, function( data ) {
        //manage the response
        manage_response(data, render_data_fields);
    });

}


/**
 * API call that builds the model and makes the predictions resulting in a list of high priority customer contacts
 * @param  {Array} fields   the field names and datatypes of the supplied csv data
 */
function build_and_predict(fields)
{

    //collect the data fields and the csv file to upload
    var data = new FormData();
    data.append('connect_ga', 'Exclude');
    data.append('fields', JSON.stringify(fields));
    data.append('file', $('#csv-input')[0].files[0]);

    $("#results-loader-card").show();
    $("#build-button").prop('disabled', true);

    //post the file and data to backend
    api_request_post_file('/api/v1/model/build', data, function(data) {
        //manage the response
        manage_response(data, render_build_model_success, render_build_model_failed, "#data-error");
    });

}


/**
 * API call to upload the resulting customer priority list (to avoid rebuilding mode) so it can be downloaded as
 * a excel file
 */
function export_to_excel()
{
    let data = JSON.stringify(result_customer_list);
    $.download('/api/v1/model/export_to_excel', 'data',data);
}