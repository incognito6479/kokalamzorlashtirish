$(document).ready(function () {
    $.ajax({
        type: 'POST',
        url: '/users/get_groups',
        dataType: "json",
        async: false,
        data: {},
        success: function (data) {
        }

    });
});