$(document).ready(function () {
    $("#id_pitomnik").select2();
    $("#id_plant").select2();
});

function ajax_plant_request(pitomnik_data) {
    let plant_url = "/pitomnik/plantedplants/ajax/plants/";
    $.ajax(
        {
            url: plant_url,
            data: pitomnik_data,
            success: function (data) {
                $("#id_plant").html(data);
            }
        });
}


function plant_request(pitomnik) {
    var pitomnik_data = {}
    if (pitomnik === true) {

        $("#id_pitomnik").change(function () {
            pitomnik_data = {
                'pitomnik': $(this).val()
            }
            ajax_plant_request(pitomnik_data)
        });
    } else {
        ajax_plant_request(pitomnik_data)
    }


}