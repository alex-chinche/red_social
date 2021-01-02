function addPick() {
    $('#add-pic-form').submit()
};

$('#add-pic-form').on('submit', function (event) {
    event.preventDefault();
    var data = new FormData($('#add-pic-form').get(0));

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
