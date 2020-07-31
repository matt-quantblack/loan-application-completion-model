/*
* A file upload component that hides the default input type=file element
*
* Author: Matthew Bailey
*
* Created: 26/07/2020
*/

$( document ).ready(function() {

    // Trigger a click on the file input field when the linked button is clicked
    $(".file-upload button").on("click", function(e) {
        e.preventDefault();
        $(this).parent().find("input").trigger("click");
    });

    // When a new file is selected update the text for this component
    $(".file-upload input").on("change", function(e) {
        var fileName = e.target.files[0].name;
        $(this).parent().find("p").text(fileName);
    });
});