$(document).ready(function() {
    $("#username").on('input', function(e) {
        $('#msg').hide();
        if($('#username').val() == null || $('#username').val() == "") {
            $('#msg').show();
            $("#msg").html("username is required!").css("color", "red");
        } else {
            $.ajax({
                type: "POST",
                url: "/register",
                data: $('#registrationform').serialize(),
                dataType: "html",
                cache: false,
                success: function(msg) {
                    $('msg').show();
                    $("#msg").html(msg);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    $('msg').show();
                    $("#msg").html(textStatus + " " + errorThrown);
                }
            });
        }
    });
});