/**
 * Created by Shubham Aggarwal on 12-11-2016.
 * Lasts uodated on 31-07-2017
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

    var nlstatus = $.cookie("nlstatus");


    function validateEmail(email) {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }

    function newsletter() {

        swal({
                title: "hackprodev Newsletter",
                text: "Chat Messages extractor Coming Soon!",
                type: "input",
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: "Enter Email Address"
            },
            function (inputValue) {
                if (inputValue === false) return false;

                if (inputValue === '') {
                    swal.showInputError("Please Enter  Email!");
                    return false;
                }

                if (!validateEmail(inputValue)) {
                    swal.showInputError("Please Enter Valid Email!");
                    return false;
                }

                var data = {
                    email: inputValue,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                };

                $.ajax({
                    type: "POST",
                    url: '/newsletter-subscribe',
                    data: data,
                    dataType: 'json',
                    success: function (data) {
                        swal("Thanks for Subscribing", "success");

                        var expDate2 = new Date();
                        expDate2.setTime(expDate2.getTime() + (30 * 24 * 60 * 60 * 1000));
                        $.cookie("nlstatus", true, {path: '/', expires: expDate2});

                    },
                    error: function () {
                        swal.showInputError("Looks like Some Error Occurred :( ");
                        return false;
                    }
                });

            });
    }


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
        if (captcha_response === '') {
            reset_id.prop('disabled', false);
            extract_id.prop('disabled', false);
            return;
        }

        // make a object of data to be send
        var data = {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "textarea": htmlcode,
            "recaptcha-response": $('#g-recaptcha-response').val()
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
        $('#id_textarea').val("");
    });


    window.onload = function () {
        setTimeout(function () {
            if (nlstatus === null || !nlstatus) {
                newsletter();
            }
        }, 2000);
    };
});