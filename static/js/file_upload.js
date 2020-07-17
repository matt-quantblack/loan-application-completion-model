
$( document ).ready(function() {
    $(".file-upload button").on("click", function(e) {
        e.preventDefault();
        $(".file-upload input").trigger("click");
    });

     $(".file-upload input").on("change", function(e) {
         var fileName = e.target.files[0].name;
         $(this).parent().find("p").text(fileName);
     });
});