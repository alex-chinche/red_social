$(document).ready(function () {
    $('#search-button').click(function () {
        find_user();
    });
});

function find_user() {
    if ($('#search-user').val().length != 0) {
        $('#search-button svg').addClass('octicon octicon-sync rotate');
        $('#search-button').prop("disabled", true);
        $('#search-button svg').show();
        setTimeout(function () {
            $.ajax({
                url: "/find_users/" + $('#search-user').val(),
                type: "GET",
                cache: true,
                dataType: 'html',

                success: function (html) {
                    $('#search_results').remove()
                    $('#search').after(html);
                    $('#search-button svg').removeClass('rotate');
                    $('#search-button svg').hide();
                },

                error: function (xhr, errmsg, err) {
                    $('#search_results').remove()
                    $('#search-button svg').removeClass('rotate');
                    $('#search-button svg').hide();
                }
            });
        }, 2000);
    }
};

function acceptFriend(acceptbutton) {
    $.ajax({
        url: "/accept_friend_request/" + $(acceptbutton).data('confirmid'),
        type: "GET",
        cache: true,
        dataType: 'json',

        success: function (html) {
            $(acceptbutton).parent().replaceWith('<div class="button-container"><p class="no-click-button right">Friend</p><br></div>');
        },

        error: function (xhr, errmsg, err) {
            console.log("error trying to accept friend")
        }
    });
}

function rejectFriendRequestReceived(rejectreceivedrequestbutton) {
    $.ajax({
        url: "/reject_friend_request_received/" + $(rejectreceivedrequestbutton).data('rejectid'),
        type: "GET",
        cache: true,
        dataType: 'json',

        success: function (html) {
            $(rejectreceivedrequestbutton).parent().replaceWith('<div class="button-container"><a class="button right" href="#" data-requesttosendid="' + $(rejectreceivedrequestbutton).data('rejectid') + '" onclick="sendFriendRequest(this)">Send request</a><br></div>');
        },

        error: function (xhr, errmsg, err) {
            console.log("error trying to reject friend")
        }
    });
};

function rejectFriendRequestSent(rejectsentrequestbutton) {
    $.ajax({
        url: "/reject_friend_request_sent/" + $(rejectsentrequestbutton).data('requestsentid'),
        type: "GET",
        cache: true,
        dataType: 'json',

        success: function (html) {
            $(rejectsentrequestbutton).replaceWith('<a class="button right" href="#" data-requesttosendid="' + $(rejectsentrequestbutton).data('requestsentid') + '" onclick="sendFriendRequest(this)">Send request</a>');
        },

        error: function (xhr, errmsg, err) {
            console.log("error trying to reject friend")
        }
    });
};

function sendFriendRequest(sendfriendbutton) {
    $.ajax({
        url: "/send_friend_request/" + $(sendfriendbutton).data('requesttosendid'),
        type: "GET",
        cache: true,
        dataType: 'json',

        success: function (html) {
            $(sendfriendbutton).replaceWith('<a class="button right" href="#" data-requestsentid="' + $(sendfriendbutton).data('requesttosendid') + '" onclick="rejectFriendRequestSent(this)">Waiting...</a>');
        },

        error: function (xhr, errmsg, err) {
            console.log("error trying to send friend request")
        }
    });
};

