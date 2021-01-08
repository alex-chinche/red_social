var fullUrl = document.URL;
url = fullUrl.substring(0, fullUrl.length - 1);
var id = url.substring(url.lastIndexOf('/') + 1);

get_user_photos(id);

function get_user_photos(id) {
    $('#profile-picture-list').html('');

    $.ajax({
        url: "/get_user_photos/" + id,
        type: "GET",
        cache: true,
        dataType: 'html',

        success: function (html) {
            if (html) {
                $('#profile-picture-list').html(html);
            }
            else {
                $('#profile-picture-list').html("<p>No photos uploaded by the user yet!</p>");
            }
        },

        error: function (xhr, errmsg, err) {
            console.log("ERROR TOMANDO FOTOS")
        }
    });
}



