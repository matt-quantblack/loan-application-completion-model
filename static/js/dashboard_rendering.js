/*
* Functions used for rending DOM using javascript
*
* Author: Matthew Bailey
*
* Created: 26/07/2020
*/


function select_option(e) {
    /*
    * Renders a dowpdown button when a dropdown item has been pressed
    *
    * Args:
    *   e (event): The click event
    */

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

function render_dropdown(selector, data) {
    /*
    * Renders dropdown items based on a list of data
    *
    * Args:
    *   selector (string): the jquery selector to select the dropdown list
    *   data (array): array of items to add, id is used as value and name is used as text
    */

    //clear the current dropdown list
    $(selector).empty();

    //add each item to the dropdown list
    data.forEach(function(val) {
        let markup = "<a class='dropdown-item' href='#' value='" + val["id"] +"'>" + val["name"] +"</a>";
        $(selector).append(markup);
    });
}

function data_file_changed() {
    /* Removes the disabled button from the build model button once a csv file has been loaded   */
    $("#build-button").prop('disabled', false);
}


/////////////////////////////////////////////////////
// Credential Uploading
/////////////////////////////////////////////////////

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

function cancel_cred_upload(e) {
    /*
    * Toggles the google analytics profile select div
    *
    * Args:
    *   e (event): click event
    */

    e.preventDefault();
    $(".google-analytics.connected").show();
    $(".google-analytics.not-configured").hide();
    $("#cancel-change-cred").hide();
}

function render_credential_upload_state() {
    /* Renders DOM showing a loading state for uploading credentials  */
    $("#credential-btn").addClass('disabled');
    $("#cred-form .details").text("Uploading new credentials file");
    $("#cred-form .ajax-loader").show();
}

function render_set_credential_success() {
    /* Renders DOM after the successful upload of new credentials  */
    $(".google-analytics.checking").show();
    $(".google-analytics.not-configured").hide();
    $("#cred-form .details").text("(Optional)");
    $("#cred-form .ajax-loader").hide();
    $("#cred-error").text("");
    $("#credential-btn").removeClass('disabled');
    check_credentials();
}

function render_set_credential_failed() {
    /* Renders DOM after the failed upload of new credentials  */
    $("#cred-form .details").text("(Optional)");
    $("#cred-form .ajax-loader").hide();
}

/////////////////////////////////////////////////////
// Checking if GA Credentials Exist
/////////////////////////////////////////////////////

function render_check_credentials_success(data) {
    /* Renders DOM after the successful checking of new credentials
    *
    * Args:
    *   data (json): the response data
    *
    */

    if(data.hasOwnProperty("result") && data["result"] == true) {
        $(".google-analytics.checking").hide();
        $(".google-analytics.getting").show();
        get_ga_profiles();
        credentials_attached = true;
    }
    else
        render_check_credentials_failed();
}

function render_check_credentials_failed() {
    /* Renders DOM after failed credential check  */

    $(".google-analytics.checking").hide();
    $(".google-analytics.not-configured").show();
    credentials_attached = false;
}

/////////////////////////////////////////////////////
// Removing GA Credentials file
/////////////////////////////////////////////////////

function render_credential_remove_state() {
    /* Renders DOM loading elements for removing credentials  */
    $(this).parent().find("img").show();
}

function render_credential_remove_success() {
    /* Renders DOM after the successful removal of credentials  */

    $(this).parent().find("img").hide();
    $(".google-analytics.connected").hide();
    $(".google-analytics.not-configured").show();
    $("#credential-upload").val(''); //clear the selected file

    credentials_attached = false;
}

/////////////////////////////////////////////////////
// Getting Google Analytics Profiles
/////////////////////////////////////////////////////
function render_get_ga_profiles_success(data) {
    /* Renders DOM after successful get of google analytics profiles
    *
    * Args:
    *   data (json): The response data
    */

    $(".google-analytics.getting").hide();
    $(".google-analytics.connected").show();
    let options = data["data"];
    options.unshift({'id': '0', 'name': 'Exclude'});
    render_dropdown("#google-analytics-select .dropdown-menu", options);
}

function render_get_ga_profiles_failed() {
    /* Renders DOM after the failed attempt of getting google analytics profiles  */

    $(".google-analytics.getting").hide();
    $("#cancel-change-cred").hide();
    $(".google-analytics.not-configured").show();
}

/////////////////////////////////////////////////////
// Data Template fields
/////////////////////////////////////////////////////

function render_data_fields(data) {
    /* Renders DOM after getting all the datatypes for the csv fields currently loaded clientside
    *
    * Args:
    *   data (json): The response data
    */

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
function render_build_model_state() {
    /* Renders loading div to show model is being built  */
    $("#build-model-loader").show();
}

function render_build_model_success(data) {
    /* Renders DOM after successful building of model - showing list of priority customers in a table
    *
    * Args:
    *   data (json): The response data
    */

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
    $("#build-model-loader").hide();

    // Scroll down to the start of results
    $("#results-card").show();
    $('html, body').animate({
            scrollTop: $("#results-card").offset().top
        }, 2000);
}

function render_build_model_failed() {
    /* Renders DOM if the model build process failed */
    $("#build-model-loader").hide();
}

function render_excel_file_success() {
    alert("Fone");
}

function render_excel_file_failed() {
    alert("Failed");
}