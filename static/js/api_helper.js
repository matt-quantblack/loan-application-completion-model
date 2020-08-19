/*
* API helper functions to simplify the common api calls
*
* Author: Matthew Bailey
*
* Created: 24/07/2020
*/

/**
 * Helper function for sending api requests with json datatype
 * @param  {String} url         The url to post to
 * @param  {JSON}   data        JSON data to be posted
 * @param  {JSON}   onsuccess   function to call if successful
 */
function api_request_post(url, data, onsuccess)
{
    $.ajax({
        url: url,
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (data) {
            onsuccess(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            server_error(errorThrown);
        }
  });
}


/**
 * Helper function for sending api requests with json datatype as well as attached files
 * @param  {String} url         The url to post to
 * @param  {JSON}   data        JSON data to be posted as FormData including file
 * @param  {JSON}   onsuccess   function to call if successful
 */
function api_request_post_file(url, data, onsuccess)
{
    //post file to api
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: onsuccess,
        error: function(jqXHR, textStatus, errorThrown) {
            server_error(errorThrown);
        }
    });
}


/**
 * Generic server error function - currently just displays in an alert box
 * @param  {String} msg     Message to display
 */
function server_error(msg)
{
    alert("Server Error: " + msg);
}


/**
 * Helper function for delegating response based on success = True/False and error
 *  fields in the response json
 * @param  {JSON} data              The response as JSON
 * @param  {Callback} on_success    Function to call if success==True
 * @param  {Callback} on_fail       Function to call if success==False
 */
function manage_response(data, on_success, on_fail, error_selector)
{
    //check for success field
    if(data.hasOwnProperty("success"))
    {
        if(data["success"] == true) {
            on_success(data)
        }
        else if(data.hasOwnProperty("error")) {
            //set the error text of the specified object
            $(error_selector).text(data["error"]);
            //render page based on fail
            if(on_fail) on_fail();
        }
        else {
            //render page based on fail
            if(on_fail) on_fail();
            server_error("Incorrect response format.");
        }
    }
    else //response is not in correct format
    {
        //render page based on fail
        if(on_fail) on_fail();
        server_error("Incorrect response format.");
    }

}
