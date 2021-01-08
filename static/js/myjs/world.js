$(document).ready(function () {
    $('#search-user').bind("change paste keyup click", function () {
        if ($('#search-user').val().length == 0) {
            $('#search-results').remove()
        }
        if ($('#search-user').val().length != 0) {
            $('#loading').addClass('octicon octicon-sync rotate');
            $('#loading').show();
            setTimeout(findUsers, 500);
        }
    });
});

function findUsers() {
    $.ajax({
        url: "/find_users/" + $('#search-user').val(),
        type: "GET",
        cache: true,
        dataType: 'html',

        success: function (html) {
            $('#search-results').remove()
            $('#search-users').after(html);
            $('#loading').removeClass('rotate');
            $('#loading').hide();
        },

        error: function (xhr, errmsg, err) {
            $('#search_results').remove()
            $('#loading').removeClass('rotate');
            $('#loading').hide();
        }
    });
}

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
            $(sendfriendbutton).replaceWith('<a class="button right" href="#" data-requestsentid="' + $(sendfriendbutton).data('requesttosendid') + '" onclick="rejectFriendRequestSent(this)">Cancel request...</a>');
        },

        error: function (xhr, errmsg, err) {
            console.log("error trying to send friend request")
        }
    });
};

