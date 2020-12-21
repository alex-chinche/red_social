$(document).ready(function () {
    $('#show-modal-register').on('click', function () {
        var now = new Date();
        var month = (now.getMonth() + 1);
        var day = now.getDate();
        if (month < 10) {
            month = "0" + month;
        }
        if (day < 10) {
            day = "0" + day;
        }
        var today = now.getFullYear() - 16 + '-' + month + '-' + day;
        $('#register-user-birthday').val(today);

        $('#registerModal').modal('show')
    });

    $('#register-form').on('submit', function (event) {
        event.preventDefault();
        $('#register-button svg').addClass('octicon octicon-sync rotate');
        $('#register-button').prop("disabled", true);
        $('#register-button svg').show();
        setTimeout(function () {
            register()
        }, 2000);
    });

    function register() {
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: "/register/",
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            cache: true,
            dataType: 'json',
            data: {
                name: $('#register-user-name').val(),
                surnames: $('#register-user-surname').val(),
                birthday: $('#register-user-birthday').val(),
                email: $('#register-user-email').val(),
                password: $('#register-user-password').val(),
                confirmPassword: $('#register-user-confirm-password').val(),
            },

            success: function (json) {
                if (json['register'] == false) {
                    if (document.getElementById('formError') == null) {
                        $('#register-form').prepend('<div id="formError" class="alert alert-warning alert-dismissible fade show" role="alert"><strong><svg viewBox="0 0 16 16" width="16" height="16"><path class="icon-warning" fill-rule="evenodd" d="M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM0 8a8 8 0 1116 0A8 8 0 010 8zm6.5-.25A.75.75 0 017.25 7h1a.75.75 0 01.75.75v2.75h.25a.75.75 0 010 1.5h-2a.75.75 0 010-1.5h.25v-2h-.25a.75.75 0 01-.75-.75zM8 6a1 1 0 100-2 1 1 0 000 2z"></path></svg> Form contains errors</strong><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
                        );
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
                    if (document.getElementById('formSuccess') == null) {
                        $('body').append('<div id="formSuccess" class="alert alert-success" role="alert"><svg viewBox="0 0 16 16" width="16" height="16"><path class="icon-check" fill-rule="evenodd" d="M1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0zM0 8a8 8 0 1116 0A8 8 0 010 8zm11.78-1.72a.75.75 0 00-1.06-1.06L6.75 9.19 5.28 7.72a.75.75 0 00-1.06 1.06l2 2a.75.75 0 001.06 0l4.5-4.5z"></path></svg> We are sending you an email to <b>' + json['email'] + '</b>. Check it!<br>Once the mail is verified, come back and login using your email and password!</div>');
                    }
                }
            },

            error: function (xhr, errmsg, err) {
                console.log("Error accessing the petition");
                if (document.getElementById('unexpectedError') == null) {
                    $('#register-form').prepend('<div id="unexpectedError" class="alert alert-danger alert-dismissible fade show" role="alert"><strong><svg viewBox="0 0 16 16" width="16" height="16"><path class="icon-warning" fill-rule="evenodd" d="M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zM0 8a8 8 0 1116 0A8 8 0 010 8zm6.5-.25A.75.75 0 017.25 7h1a.75.75 0 01.75.75v2.75h.25a.75.75 0 010 1.5h-2a.75.75 0 010-1.5h.25v-2h-.25a.75.75 0 01-.75-.75zM8 6a1 1 0 100-2 1 1 0 000 2z"></path></svg> Unexpected error</strong><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
                    );
                }
                $('#register-button svg').removeClass('rotate');
                $('#register-button').prop("disabled", false);
                $('#register-button svg').hide();
            }
        });
    };
});