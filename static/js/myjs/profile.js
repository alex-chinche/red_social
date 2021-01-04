function get_photos() {
    $('#profile-picture-list').html('');

    $.ajax({
        url: "/get_my_photos/",
        type: "GET",
        cache: true,
        dataType: 'html',

        success: function (html) {
            $('#profile-picture-list').html(html);
        },

        error: function (xhr, errmsg, err) {
            console.log("ERROR TOMANDO FOTOS")
        }
    });
}

get_photos();

function addProfilePick() {
    $('#add-profile-pic-form').submit()
};

$('#add-profile-pic-form').on('submit', function (event) {
    event.preventDefault();
    var data = new FormData($('#add-profile-pic-form').get(0));

    setTimeout(function () {
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: "/upload_profile_pic/",
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            cache: true,
            dataType: 'json',
            data: data,
            processData: false,
            contentType: false,

            success: function (json) {
                $(profile_pic).attr('src', '/media/' + json['path']);
            },

            error: function (xhr, errmsg, err) {
                console.log("Error accessing the petition");
            }
        });
    }, 2000);
});

function addPick() {
    $('#add-pic-form').submit()
};

$('#add-pic-form').on('submit', function (event) {
    event.preventDefault();
    var data = new FormData($('#add-pic-form').get(0));

    setTimeout(function () {
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: "/upload_photo/",
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            cache: true,
            dataType: 'json',
            data: data,
            processData: false,
            contentType: false,

            success: function (json) {
                get_photos();
            },

            error: function (xhr, errmsg, err) {
                console.log("Error accessing the petition");
            }
        });
    }, 2000);
});

