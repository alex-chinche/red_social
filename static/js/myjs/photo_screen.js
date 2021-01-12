$('#change_description').on('click', function () {
    $('#description_form').fadeToggle(100);
});

$('#hide_description').on('click', function () {
    $('#description_form').fadeOut(100);
});

function delete_photo() {
    $('#loading').addClass('octicon octicon-sync rotate');
    $('#loading').show();
    setTimeout(delete_photo_request, 1500);
}

function delete_photo_request() {
    $.ajax({
        url: "/delete_photo/" + $('#delete_photo_button').attr("data-photoid"),
        type: "GET",
        cache: true,
        dataType: 'json',

        success: function (html) {
            document.location.href = "/myprofile/";
        },

        error: function (xhr, errmsg, err) {
            $('#loading').removeClass('rotate');
            $('#loading').hide();
        }
    });
}