read_header = function (file, on_complete) {

    var reader = new FileReader();

    reader.onload = function () {
        let lines = reader.result.split("\n");
        let header = lines[0].split(",");
        on_complete(header);
    };

    // start reading the file. When it is done, calls the onload event defined above.
    reader.readAsBinaryString(file);
};

display_header = function(fields) {
    let render_table = $("table.csv-parser");
    let render_table_body = render_table.find("tbody");

    let template_row =  render_table_body.find("tr:first");
    let template_row_html = "<tr>" + template_row.html() + "</tr>";


    if(fields.length > 0) {
        template_row.hide();
        render_table.show();
    }
    else
        render_table.hide();

    fields.forEach(function(val) {
        let markup = template_row_html.replace("[[field_name]]", val);
        render_table_body.append(markup);
    });

};


$( document ).ready(function() {
    $("input.csv-parser").on("change", function (e) {
        read_header(e.target.files[0], display_header);
    });
});