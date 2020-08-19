/*
* Functions used for rending DOM using javascript
*
* Author: Matthew Bailey
*
* Created: 26/07/2020
*/

/**
 * Renders a dowpdown button when a dropdown item has been pressed
 * @param  {Event} e The click event
 */
function select_option(e) {

    //prevent page reload
    e.preventDefault();

    //get the details from the dropdown item
    let value = $(this).attr('value');
    let text = $(this).text();

    //get the dropdown button
    let selection = $(this).parent().parent().find("button");

    //store these in the dropdown button
    selection.attr("value", value);
    selection.text(text);
}


/**
 * Renders dropdown items based on a list of data
 * @param  {String} selector The jquery selector to select the dropdown list
 * @param  {Array}   data     Array of items to add, id is used as value and name is used as text
 */
function render_dropdown(selector, data) {

    //clear the current dropdown list
    $(selector).empty();

    //add each item to the dropdown list
    data.forEach(function(val) {
        let markup = "<a class='dropdown-item' href='#' value='" + val["id"] +"'>" + val["name"] +"</a>";
        $(selector).append(markup);
    });
}


/**
 * Removes the disabled button from the build model button once a csv file has been loaded
 */
function data_file_changed() {
    $("#build-button").prop('disabled', false);
}


/////////////////////////////////////////////////////
// Credential Uploading
/////////////////////////////////////////////////////


/**
 * Toggles the upload credentials div
 * @param  {Event} e The click event
 */
function show_cred_upload(e) {
    /*
    * Toggles the upload credentials div
    *
    * Args:
    *   e (event): click event
    */
    e.preventDefault();
    $(".google-analytics.connected").hide();
    $(".google-analytics.not-configured").show();
    $("#cancel-change-cred").show();
}


/**
 * Toggles the google analytics profile select div
 * @param  {Event} e The click event
 */
function cancel_cred_upload(e) {

    e.preventDefault();
    $(".google-analytics.connected").show();
    $(".google-analytics.not-configured").hide();
    $("#cancel-change-cred").hide();
}


/**
 * Renders DOM showing a loading state for uploading credentials
 */
function render_credential_upload_state() {

    $("#credential-btn").addClass('disabled');
    $("#cred-form .details").text("Uploading new credentials file");
    $("#cred-form .ajax-loader").show();
}


/**
 * Renders DOM after the successful upload of new credentials
 */
function render_set_credential_success() {

    $(".google-analytics.checking").show();
    $(".google-analytics.not-configured").hide();
    $("#cred-form .details").text("(Optional)");
    $("#cred-form .ajax-loader").hide();
    $("#cred-error").text("");
    $("#credential-btn").removeClass('disabled');
    check_credentials();
}


/**
 * Renders DOM after the failed upload of new credentials
 */
function render_set_credential_failed() {
    $("#cred-form .details").text("(Optional)");
    $("#cred-form .ajax-loader").hide();
}

/////////////////////////////////////////////////////
// Checking if GA Credentials Exist
/////////////////////////////////////////////////////


/**
 * Renders DOM after the successful checking of new credentials
 * @param  {JSON} data The response data
 */
function render_check_credentials_success(data) {

    if(data.hasOwnProperty("result") && data["result"] == true) {
        $(".google-analytics.checking").hide();
        $(".google-analytics.getting").show();
        get_ga_profiles();
        credentials_attached = true;
    }
    else
        render_check_credentials_failed();
}


/**
 * Renders DOM after failed credential check
 */
function render_check_credentials_failed() {

    $(".google-analytics.checking").hide();
    $(".google-analytics.not-configured").show();
    credentials_attached = false;
}

/////////////////////////////////////////////////////
// Removing GA Credentials file
/////////////////////////////////////////////////////


/**
 * Renders DOM loading elements for removing credentials
 */
function render_credential_remove_state() {
    $(this).parent().find("img").show();
}


/**
 * Renders DOM after the successful removal of credentials
 */
function render_credential_remove_success() {

    $(this).parent().find("img").hide();
    $(".google-analytics.connected").hide();
    $(".google-analytics.not-configured").show();
    $("#credential-upload").val(''); //clear the selected file

    credentials_attached = false;
}

/////////////////////////////////////////////////////
// Getting Google Analytics Profiles
/////////////////////////////////////////////////////


/**
 * Renders DOM after successful get of google analytics profiles
 * @param  {JSON} data The response data
 */
function render_get_ga_profiles_success(data) {

    $(".google-analytics.getting").hide();
    $(".google-analytics.connected").show();
    let options = data["data"];
    options.unshift({'id': '0', 'name': 'Exclude'});
    render_dropdown("#google-analytics-select .dropdown-menu", options);
}


/**
 * Renders DOM after the failed attempt of getting google analytics profiles
 */
function render_get_ga_profiles_failed() {

    $(".google-analytics.getting").hide();
    $("#cancel-change-cred").hide();
    $(".google-analytics.not-configured").show();
}

/////////////////////////////////////////////////////
// Data Template fields
/////////////////////////////////////////////////////

/**
 * Renders DOM after getting all the datatypes for the csv fields currently loaded clientside
 * @param  {JSON} data The response data
 */
function render_data_fields(data) {

    data.data.forEach(function(val) {
        //get the dropdown item that matches this field name
        let item = $(".data-member").filter(function(){
          return $(this).text().trim() === val[0].trim();
        }).parent().find(".dropdown-toggle");

        //set the text and value to the data supplied
        item.text(val[1]);
        item.attr('value', val[2]);
    });
}


/////////////////////////////////////////////////////
// Building model and displaying results
/////////////////////////////////////////////////////

/**
 * Renders loading div to show model is being built
 */
function render_build_model_state() {
    $("#build-model-loader").show();
}


/**
 * Renders DOM after successful building of model - showing list of priority customers in a table
 * @param  {JSON} data The response data
 */
function render_build_model_success(data) {

    let isFirst = true; // used to determine header information

    // clear the current table
    $("#results-table thead").empty();
    $("#results-table tbody").empty();

    //store in a global variable so can be easily reuploaded to export to excel
    result_customer_list = data.data;

    // go through each customer returned
    result_customer_list.forEach(function (obj) {

        // get the fields from this entry
        let fields = Object.keys(obj);

        // on first run fill out the table header with field names
        if(isFirst)
        {
            isFirst = false;
            let markup = "";
            fields.forEach(function(field) {
                markup += "<th>" + field + "</th>";
            });

            $("#results-table thead").append(markup);
        }

        // Create a row for each customer and render all details
        let markup = "<tr>";
        fields.forEach(function(field) {
            markup += "<td>" + obj[field] + "</td>";
        });
        markup += "</tr>";

        $("#results-table tbody").append(markup);
    });

    // Hide the loading div
    $("#results-loader-card").hide();
    $("#build-button").prop('disabled', false);

    // Scroll down to the start of results
    $("#results-card").show();
    $('html, body').animate({
            scrollTop: $("#results-card").offset().top
        }, 2000);


}


/**
 * Renders DOM if the model build process failed
 */
function render_build_model_failed() {
    // Hide the loading div
    $("#results-loader-card").hide();
    $("#build-button").prop('disabled', false);
}


/**
 * Simple alert success
 */
function render_excel_file_success() {
    alert("Done");
}


/**
 * Simple alert error
 */
function render_excel_file_failed() {
    alert("Failed");
}