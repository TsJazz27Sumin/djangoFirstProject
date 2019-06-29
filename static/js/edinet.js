$(document).ready(function () {
    $("#try-ajax").click(function () {

        targetUrl = window.location.href + this.name.replace("/", "");

        $.ajax({
            type: "GET",
            url: targetUrl,
            dataType: "json"
        }).done(function (data) {
            alert(data.message);
        });
    });
});