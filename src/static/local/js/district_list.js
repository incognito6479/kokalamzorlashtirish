let id_region = document.getElementById("id_region")
let id_district = document.getElementById("id_district")
let district_value = id_district.options[id_district.selectedIndex].value;
console.log(district_value)

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

set_district();

id_region.addEventListener("change", function (e) {
    set_district();
})