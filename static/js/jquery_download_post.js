/*
* Awesome bit of clever code that allows downloading a file from an ajax post
*
* Author: Matthew Bailey (found on internet https://gist.github.com/DavidMah/3533415)
*
* Created: 31/07/2020
*/

// Takes a URL, param name, and data string
// Sends to the server.. The server can respond with binary data to download
jQuery.download = function(url, key, data){
    // Build a form
    let form = $('<form></form>').attr('action', url).attr('method', 'post');
    // Add the one key/value
    form.append($("<input></input>").attr('type', 'hidden').attr('name', key).attr('value', data));
    //send request
    form.appendTo('body').submit().remove();
};