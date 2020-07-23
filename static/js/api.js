function api_request_post(url, data, onsuccess)
{
    $.ajax({
        url: url,
        data: data,
        dataType: 'json',
        success: function (data) {
            onsuccess(data);
        }
  });
}

function render_dropdown(selector, data) {

    $(selector).empty();

    data.forEach(function(val) {
        let markup = "<a class='dropdown-item' href='#' value='" + val["id"] +"'>" + val["name"] +"</a>";
        $(selector).append(markup);
    });
}

function set_credentials(e) {

    var button = $("#credential-btn");
    button.addClass('disabled');

    var data = new FormData($('form').get(0));
    $("#cred-form .details").text("Uploading new credentials file");
    $("#cred-form .ajax-loader").show();

    $.ajax({
        url: '/api/v1/ga/cred_set',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data) {
            button.removeClass('disabled');

            if(data.hasOwnProperty("error")) {
                alert(data["error"]);
                $("#cred-form .details").text("(Optional)");
                $("#cred-form .ajax-loader").hide();
            }
            else
            {
                $(".google-analytics.checking").show();
                $(".google-analytics.not-configured").hide();
                check_credentials();
            }
        }
    });
}

function get_ga_profiles() {
    $.get("/api/v1/ga/profiles/all", function( data ) {

        $(".google-analytics.getting").hide();

        if(data.hasOwnProperty("success") && data["success"] == true)
        {
            $(".google-analytics.connected").show();
            let options = data["data"];
            options.unshift({'id': '0', 'name': 'Exclude'});

            render_dropdown("#google-analytics-select .dropdown-menu", options)

        }
        else {
            $(".google-analytics.not-configured").show();
        }
    });
}

function check_credentials()
{
    $.get("/api/v1/ga/check_cred", function( data ) {

        $(".google-analytics.checking").hide();

        if(data.hasOwnProperty("success") && data["success"] == true)
        {
            $(".google-analytics.getting").show();
            get_ga_profiles();
        }
        else {
            $(".google-analytics.not-configured").show();
        }
    });
}


function get_data_template(fields)
{
    var get_data = "?";

    fields.forEach(function(val) {
       get_data += "name=" + val + "&";
    });

    $.get("/api/v1/data_template/find" + get_data, function( data ) {

        if(data.hasOwnProperty("success") && data["success"] == true)
        {
            data.data.forEach(function(val) {
                $(".data-member").filter(function(){
                  return $(this).text().trim() === val[0].trim();
                }).parent().find(".dropdown-toggle").text(val[1]);
            });
        }

    });
}
