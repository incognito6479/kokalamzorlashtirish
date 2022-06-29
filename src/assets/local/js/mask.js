$(document).ready(function () {
    $.mask.definitions['9'] = false;
    $.mask.definitions['*'] = "[0-9]";
    $('#phone').mask('+998(**) ***-**-**');
})

$(document).ready(function () {
    $.mask.definitions['9'] = false;
    $.mask.definitions['*'] = "[0-9]";
    $('#during').mask('*****.**');
})