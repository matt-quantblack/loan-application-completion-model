
select_option = function() {
    let value = $(this).attr('value');
    let text = $(this).text();
    selection = $(this).parent().parent().find("button");

    selection.attr("value", value);
    selection.text(text);
}

$( document ).ready(function() {
    $(".dropdown-menu .dropdown-item").on("click", select_option);

    $("table.csv-parser").on("click", ".dropdown-menu .dropdown-item", select_option);
});