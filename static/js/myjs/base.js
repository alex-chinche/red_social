/*
setInterval(sendPulse, 10000);
setInterval(getFriendList, 10000);
*/

function getFriendList() {
    $.ajax({
        url: "/get_friend_list/",
        type: "GET",
        async: true,
        dataType: 'json',
        success: function (html) {
            $('#chat-inside').html(html['friends_html'])
            $('#friends-connected').html('(' + html['number_of_connected_friends'] + ')');
            $('#number-of-friends').html('Friends (' + html['number_of_friends'] + ')');
        },
        error: function (xhr, errmsg, err) {
            console.log("Error in pulse request")
        }
    });
}

function sendPulse() {
    $.ajax({
        url: "/pulse/",
        type: "GET",
        async: true,
        dataType: 'json',
        error: function (xhr, errmsg, err) {
            console.log("Error in pulse request")
        }
    });
}
$(document).ready(function () {
    sendPulse();
    getFriendList();
    $('#logout').click(function () {
        logout();
    });

    function logout() {
        $.ajax({
            url: "/logout/",
            type: "GET",
            cache: true,
            dataType: 'html',
            success: function (html) {
                document.location.href = "/";
            },

            error: function (xhr, errmsg, err) {
                console.log("Error trying to logout")
            }
        });
    }
});
function hideChat(button) {
    $('#chat-col').css("transform", "translateX(300px)");
    $('#chat-col').css("transition", ".5s");
    $('#change-chat svg').replaceWith('<svg viewBox="0 0 16 16" width="12" height="12"><path fill-rule="evenodd" d="M7.78 12.53a.75.75 0 01-1.06 0L2.47 8.28a.75.75 0 010-1.06l4.25-4.25a.75.75 0 011.06 1.06L4.81 7h7.44a.75.75 0 010 1.5H4.81l2.97 2.97a.75.75 0 010 1.06z"></path></svg>')
    $("#change-chat").attr("onclick", "showChat()");
}
function showChat(button) {
    $('#change-chat svg').replaceWith('<svg viewBox="0 0 16 16" width="12" height="12"><path fill-rule="evenodd" d="M8.22 2.97a.75.75 0 011.06 0l4.25 4.25a.75.75 0 010 1.06l-4.25 4.25a.75.75 0 01-1.06-1.06l2.97-2.97H3.75a.75.75 0 010-1.5h7.44L8.22 4.03a.75.75 0 010-1.06z"></path></svg>')
    setTimeout(function () {
        $('#chat-col').css("transform", "translateX(0px)");
        $('#chat-col').css("transition", ".5s");
        $("#change-chat").attr("onclick", "hideChat()");
    }, 20);
}