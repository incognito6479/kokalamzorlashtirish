$(document).ready(function () {
    $("#id_road_district").select2();
});
$("#id_district").change(function () {
    let road_url = "/pitomnik/plantedplants/ajax/roads/";
    let districtId = $(this).val();
    $.ajax({
        url: road_url,
        data: {
            'district': districtId
        },
        success: function (data) {
            $("#id_road_district").html(data);
        }
    });
});