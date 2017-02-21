/**
 * Created by Shubham Aggarwal on 12-11-2016.
 */

var effect = [
    "bounce",
    "pulse",
    "rubberBand",
    "shake",
    "headShake",
    "swing",
    "tada"
];

$(document).ready(function () {

    // over on top heading
    // animation effects using animate.cs
    $('#heading').hover(function () {
        $(this).removeClass();
        var index = Math.floor((Math.random() * 10) + 1);
        $(this).addClass('animated ' + effect[index - 1]);
    }, function () {
        $(this).removeClass();
    });

    $("#id_divform").submit(function (event) {
        // prevent for default submitting form
        event.preventDefault();

        var extract_id = $('#extract');
        var reset_id = $('#reset');

        // disable buttons
        extract_id.prop('disabled', true);
        reset_id.prop('disabled', true);

        // get htmlcode from which contacts extracted
        var htmlcode = $('#id_textarea').val();
        var captcha_response = $('#g-recaptcha-response').val();

        // captcha checked or not
        if(captcha_response == '') {
            alert("You need to fill Recaptcha First to Proof that you are a Human !");
            reset_id.prop('disabled', false);
            extract_id.prop('disabled', false);
            return ;
        }

        // make a object of data to be send
        var data = {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "textarea": htmlcode,
            "recaptcha-response" : $('#g-recaptcha-response').val()
        };

        // ajax request to server
        $.ajax({
            type: "POST",
            url: '/',
            data: data,
            dataType: 'json',
            success: function (response) {
                var msg = " Volia ! You have " + response["count"].toString() + " Contacts . Check your downloads";
                $('#success-message').html(msg);
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

        // enable buttons
        reset_id.prop('disabled', false);
        extract_id.prop('disabled', false);
    });

    // reset textarea
    $("#reset").on("click", function () {
        $('#div-element').val("");
    });
});