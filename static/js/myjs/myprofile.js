
function get_photos() {
    $.ajax({
        url: "/get_my_photos/",
        type: "GET",
        cache: true,
        dataType: 'html',

        success: function (html) {
            $('#content').html(html);
        },

        error: function (xhr, errmsg, err) {
            console.log("ERROR TOMANDO FOTOS")
        }
    });
}

function get_friends() {
    $.ajax({
        url: "/get_friends/",
        type: "GET",
        cache: true,
        dataType: 'json',

        success: function (html) {
            $('#content').html(html['friends']);
        },

        error: function (xhr, errmsg, err) {
            console.log("ERROR")
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
                $('#profile_main_image').css('background-image', 'url("/media/' + json['path'] + '")');
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

