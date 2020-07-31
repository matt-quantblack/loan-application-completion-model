/*
* API helper functions to simplify the common api calls
*
* Author: Matthew Bailey
*
* Created: 24/07/2020
*/

function api_request_post(url, data, onsuccess)
{
    /* Helper function for sending api requests with json datatype
    *  Args:
    *   url: The url to post to
    *   data: JSON data to be posted
    *   onsuccess: function to call if successful
    */

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

function api_request_post_file(url, data, onsuccess)
{
    /* Helper function for sending api requests with json datatype as well as attached files
    *  Args:
    *   url: The url to post to
    *   data: JSON data to be posted as FormData including file
    *   onsuccess: function to call if successful
    */

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

function server_error(msg)
{
    /* Generic server error function - currently just displays in an alert box
    *  Args:
    *   msg: Msg to display
    */

    alert("Server Error: " + msg);
}

function manage_response(data, on_success, on_fail, error_selector)
{
    /* Helper function for delegating response based on success = True/False and error
    *  fields in the response json
    *  Args:
    *   data: Teh response as JSON
    *   on_success: function to call if success==True
    *   on_fail: function to call if success==False
    */

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
