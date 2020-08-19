/*
* Module to parse CSV file headers on client side and render details to HTML page
*
* Author: Matthew Bailey
*
* Created: 24/07/2020
*/

/**
 * Reads the first line of a csv file
 * @param  {String}     file the file object to parse
 * @param  {Callback}   on_complete function to run once successful
 */
read_header = function (file, on_complete) {
    //create a file reader
    var reader = new FileReader();

    //define the function to run once loaded
    reader.onload = function () {

        //get all lines from csv - an speed this up by reading one line at a time
        let lines = reader.result.split("\n");

        // get the first line as the header
        let header = lines[0].split(",");

        //run the on_complete function
        on_complete(header);
    };

    // start reading the file. When it is done, calls the onload event defined above.
    reader.readAsBinaryString(file);
};


/**
 * Renders the header fields into HTML
 * @param  {Array} fields the string fields from the header line of the csv
 */
display_header = function(fields) {
    /*
    * Renders the header fields into HTML
    *
    * Args:
    *   fields: the string fields from the header line of the csv
    */

    // Collect the required HTML objects from the DOM

    // Table to render results
    let render_table = $("table.csv-parser");
    let render_table_body = render_table.find("tbody");

    // First row of table is used as a template row
    let template_row =  render_table_body.find("tr:first");
    let template_row_html = "<tr>" + template_row.html() + "</tr>";

    // Clear the table and reappend the template row
    render_table_body.empty();
    render_table_body.append(template_row_html);
    template_row =  render_table_body.find("tr:first");

    // Hide the table if there are no fields to show
    if(fields.length > 0) {
        template_row.hide();
        render_table.show();
    }
    else
        render_table.hide();

    // Create the markup for each field and append to the table
    fields.forEach(function(val) {

        //create the markup from the template row
        let markup = template_row_html.replace("[[field_name]]", val);

        //add to the table
        render_table_body.append(markup);
    });

    //call api to auto fill the default value types
    get_data_template(fields);

};


//listen for a new file selection on this csv parser to start the parsing function
$( document ).ready(function() {
    $("input.csv-parser").on("change", function (e) {
        read_header(e.target.files[0], display_header);
    });
});