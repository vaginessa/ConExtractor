/**
 * Created by Shubham Aggarwal on 12-11-2016.
 */
$(document).ready(function () {

    $("#extract").on("click", function () {

        $('#extract').prop('disabled', true);
        $('#reset').prop('disabled', true);
        var htmlcode = $('#div-element').val();

        if(htmlcode==""){
            $('#error-message').val("You Cannot Submit Empty Div Element !");
            $('.modal').modal();
            $('#error-modal').modal('open');
            return ;
        }

        var data = {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "htmlcode": htmlcode
        };

        $.ajax({
            type: "POST",
            url: '/',
            data: data,
            dataType : 'json',
            success: function (response) {
                $('#success-message').val(" Volia ! You have " + response["count"] + " Contacts . Check your downloads");
                $('.modal').modal();
                $('#success-modal').modal('open');
                var file = new File([response["contacts"]], "Contact-List.txt", {type: "text/plain;charset=utf-8"});
                saveAs(file);
            },
            error: function () {
                $('#error-message').val("Server not Responding !");
                $('.modal').modal();
                $('#error-modal').modal('open');
            }
        });

        $('#reset').prop('disabled', false);
        $('#extract').prop('disabled', false);
    });

    $("#reset").on("click", function () {
        $('#div-element').val("");
    });
});