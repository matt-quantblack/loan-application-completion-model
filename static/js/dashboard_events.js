/*
* Event listeners for the dashboard page
*
* Author: Matthew Bailey
*
* Created: 26/07/2020
*/

$( document ).ready(function() {

    // Call the api to determine if Google Analytics credentials are active
    check_credentials();

    // Dropdown box selection sets button to text
    $("#details-table").on("click", ".dropdown-menu .dropdown-item", select_option);

    // Dropdown box selection in the fields table
    $("table.csv-parser").on("click", ".dropdown-menu .dropdown-item", select_option);

    // Click button to upload new credentials
    $("#details-table").on("change", "#credential-upload", set_credentials);

    // Click button to remove credentials from local file storage
    $("#remove-cred").on("click", check_remove_cred);

    // Click button to build and run model
    $("#build-button").on("click", build);

    // Click button to build and run model
    $("#export-button").on("click", export_to_excel);

    // Watch for new selection of the data file csv
    $("input.csv-parser").on("change", data_file_changed);

    // Toggle display for uploading new credentials and selecting profiles from Google Analytics
    $("#change-cred").on("click", show_cred_upload);
    $("#cancel-change-cred").on("click", cancel_cred_upload);


});