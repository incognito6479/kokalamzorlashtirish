let id_region = document.getElementById("id_region")
let id_district = document.getElementById("id_district")


function set_district() {
    let distirct_url = "/pitomnik/plantedplants/ajax/districts/";
    let regionId = id_region.value;
    $.ajax({
        url: distirct_url,
        data: {
            'region': regionId
        },
        success: function (data) {
            $("#id_district").html(data);
        }
    });
}

$("#id_district").select2();
if(id_region.value!="" && id_district.value===""){
    set_district();
}


id_region.addEventListener("change", function (e) {
    set_district();
})