
select_option = function(e) {

    e.preventDefault();

    let value = $(this).attr('value');
    let text = $(this).text();
    selection = $(this).parent().parent().find("button");

    selection.attr("value", value);
    selection.text(text);
};

data_file_changed = function() {
    $("#build-button").show();
};

build = function() {
    build_and_predict();
};

$( document ).ready(function() {

    //Call the api to determine if Google Analytics credentials are active
    check_credentials();

    $("#details-table").on("click", ".dropdown-menu .dropdown-item", select_option);

    $("#details-table").on("change", "#credential-upload", set_credentials);

    $("table.csv-parser").on("click", ".dropdown-menu .dropdown-item", select_option);

    $("input.csv-parser").on("change", data_file_changed);

    $("#build-button").on("click", build);
});