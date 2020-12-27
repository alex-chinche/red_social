$(document).ready(function () {
    window.onscroll = function () { myFunction() };
    var navbar = document.getElementById("navbar");
    var sticky = navbar.offsetTop;
    $('#logout').click(function () {
        logout();
    });
    function myFunction() {
        if (window.pageYOffset >= sticky) {
            navbar.classList.add("sticky")
        } else {
            navbar.classList.remove("sticky");
        }
    }

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