$(document).ready(function () {
    $('#show-modal-login').on('click', function () {
        $('#loginModal').modal('show')
    });

    $('#login-form').on('submit', function (event) {
        event.preventDefault();
        $('#login-button svg').addClass('octicon octicon-sync rotate');
        $('#login-button').prop("disabled", true);
        $('#login-button svg').show();
        setTimeout(function () {
            login()
        }, 2000);
    });

    function login() {
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
                email: $('#login-user-email').val(),
                password: $('#login-user-password').val(),
            },

            success: function (json) {
                if (json['login'] == false) {
                    if (document.getElementById('formError') == null) {
                        $('#login-form').prepend('<div id="formError" class="alert alert-warning alert-dismissible fade show" role="alert"><strong><svg viewBox="0 0 16 16" width="16" height="16"><path class="icon-warning" fill-rule="evenodd" d="M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM0 8a8 8 0 1116 0A8 8 0 010 8zm6.5-.25A.75.75 0 017.25 7h1a.75.75 0 01.75.75v2.75h.25a.75.75 0 010 1.5h-2a.75.75 0 010-1.5h.25v-2h-.25a.75.75 0 01-.75-.75zM8 6a1 1 0 100-2 1 1 0 000 2z"></path></svg> Invalid data</strong><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
                        );
                    }
                    $('#login-button svg').removeClass('rotate');
                    $('#login-button').prop("disabled", false);
                    $('#login-button svg').hide();
                }
                else if (json['login'] == true) {
                    document.cookie = 'auth_token=' + json['token'];
                    $('#loginModal').modal('hide')
                    $('#login-button svg').removeClass('rotate');
                    $('#login-button').prop("disabled", false);
                    $('#login-button svg').hide();
                }
            },

            error: function (xhr, errmsg, err) {
                console.log("Error accessing the petition");
                if (document.getElementById('unexpectedError') == null) {
                    $('#login-form').prepend('<div id="unexpectedError" class="alert alert-danger alert-dismissible fade show" role="alert"><strong><svg viewBox="0 0 16 16" width="16" height="16"><path class="icon-warning" fill-rule="evenodd" d="M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM0 8a8 8 0 1116 0A8 8 0 010 8zm6.5-.25A.75.75 0 017.25 7h1a.75.75 0 01.75.75v2.75h.25a.75.75 0 010 1.5h-2a.75.75 0 010-1.5h.25v-2h-.25a.75.75 0 01-.75-.75zM8 6a1 1 0 100-2 1 1 0 000 2z"></path></svg> Unexpected error</strong><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
                    );
                }
                $('#login-button svg').removeClass('rotate');
                $('#login-button').prop("disabled", false);
                $('#login-button svg').hide();
            }
        });
    };
});