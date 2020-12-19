$(document).ready(function () {
    console.log("ready!");
    var formError = '<div id="formError" class="alert alert-warning alert-dismissible fade show" role="alert"><strong><svg viewBox="0 0 16 16" width="16" height="16"><path class="icon-warning" fill-rule="evenodd" d="M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM0 8a8 8 0 1116 0A8 8 0 010 8zm6.5-.25A.75.75 0 017.25 7h1a.75.75 0 01.75.75v2.75h.25a.75.75 0 010 1.5h-2a.75.75 0 010-1.5h.25v-2h-.25a.75.75 0 01-.75-.75zM8 6a1 1 0 100-2 1 1 0 000 2z"></path></svg> Form contains errors</strong><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
    $('#register-form').on('submit', function (event) {
        event.preventDefault();
        $('#register-button svg').addClass('octicon octicon-sync rotate');
        $('#register-button').prop("disabled", true);
        $('#register-button svg').show();
        setTimeout(function () {
            register()
        }, 3000);
    });

    function register() {
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: "/login/",
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            cache: true,
            dataType: 'json',
            data: {
                name: $('#user-name').val(),
                surnames: $('#user-surname').val(),
                birthday: $('#user-birthday').val(),
                email: $('#user-email').val(),
                password: $('#user-password').val(),
                confirmPassword: $('#user-confirm-password').val(),
            },

            success: function (json) {
                if (json['register'] == false) {
                    if (document.getElementById('formError') == null) {
                        $('#register-form').prepend(formError);
                    }
                    $('#register-button svg').removeClass('rotate');
                    $('#register-button').prop("disabled", false);
                    $('#register-button svg').hide();
                }
                else if (json['register'] == true) {
                    $('#registerModal').modal('hide')
                    $('#register-button svg').removeClass('rotate');
                    $('#register-button').prop("disabled", false);
                    $('#register-button svg').hide();
                }
            },

            error: function (xhr, errmsg, err) {
                console.log("Error accessing the petition");
            }
        });
    };


});