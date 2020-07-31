/*
* Dashboard page functionality
*
* Author: Matthew Bailey
*
* Created: 26/07/2020
*/

//global variable to store if the google analytics credentials are installed in the file system
let credentials_attached = false;
//global variable to store the resulting customer list locally for easy reupload
let result_customer_list = [];

function gather_fields() {
    /* Gets the field names and data types from the DOM
    *
    * Returns:
    *   fields (array): An array of each field
    *
    */

    // Gather field data types
    let fields = [];
    $(".data-member:visible").each(function() {
        // Name of field
        let field_name = $(this).text().trim();
        // The text value for data type
        let text = $(this).parent().find(".dropdown-toggle").text().trim();
        // The interger value for data type
        let value = parseInt($(this).parent().find(".dropdown-toggle").attr('value'));
        //push to array
        fields.push([field_name, text, value]);
    });

    return fields;
}

validate_data = function(fields) {
    /*
    * Validates the data before building the model
    * Data Requirements:
    * Must have only one response variable
    * All fields must have a selection
    * If GA credentials are installed a profile must be selected
    * GA Merge variable required if Google Analytics is not excluded
    * Server side will validate correct data types eg. Numeric and percentage are numbers, Yes/No contain only yes/no
    *
    * Args:
    *   fields (array): An array of each field
    *
    * Returns:
    *   True if no errors otherwise false
    */

    // Array to hold errors
    let errors = [];
    // Count how many response and merge variables
    let responseVariable = 0;
    let mergeVariable = 0;

    // Go through all fields and check types
    fields.forEach(function (val) {
        // extract the data type and field name
        let dtype = val[2];
        let field = val[0];

        if(dtype == 8) // Count GA merge variables
        {
            mergeVariable += 1;
            if(mergeVariable > 1)
                errors.push("Only one Google Analytics merge variable allowed: Duplicate found at " + field);
        }
        else if(dtype == 9) // Count response variables
        {
            responseVariable += 1;
            if(responseVariable > 1)
                errors.push("Only one response variable allowed: Duplicate found at " + field);
        }
        if(dtype == -1) // No selection made
        {
            errors.push("Data type must be provided for all fields: Missing at " + field);
        }
    });

    // Must have a response variable
    if(responseVariable == 0)
        errors.push("There must be at least one response variable tagged.");

    // Check if the google credentials are attached - if they are we need to check a profile was selected
    if(credentials_attached) {
        // Get selected profile
        let selected_profile = $("#google-analytics-select").find(".dropdown-toggle").attr('value');

        // No selection
        if(selected_profile == "-1")
            errors.push("You must select a google analytics profile or select Exclude to omit this data.");

        // Check for GA merge variable - must be only one
        else if (selected_profile != "0") {
            if(mergeVariable == 0)
                errors.push("You must have a Google Analytics merge variable or Exclude the GA data.");
        }
    }


    // Render errors to page
    $("#data-error").empty();
    errors.forEach(function(err) {
        $("#data-error").append($("<li>" + err + "</li>"));
    });

    // Return true if no errors
    return (errors.length === 0);

};

function build() {
    /* After validating data will build the model   */

    //get the fields from the DOM
    let fields = gather_fields();

    //Validate data and if good build model
    if(validate_data(fields))
        build_and_predict(fields);
}

function check_remove_cred(e) {
    /*
    * Checks if the user really wants to delete the credentials file
    *
    * Args:
    *   e (event): The click event
    */

    //stop page reload
    e.preventDefault();

    //window to confirm
    if(window.confirm("Are you sure you want to delete the google analytics credentials currently stored on the system?"))
        //confirmed so send api call to delete credentials
        remove_credentials();
}

