function remove_quantity_validation() {
    $("#quantity_span").removeClass("text-danger").empty();
    $("#submit-id-submit").prop("disabled", false);
}

function show_quantity_and_change_button_property(quantity_id) {
    let max_quantity = $("#id_plant").find(':selected').attr('quantity');
    $("#quantity_span").text(`Бу ўсимликдан ${~~max_quantity} дона қолган`);
    quantity_id.addEventListener("change", function (e) {
        let max_quantity = $("#id_plant").find(':selected').attr('quantity');
        let entered_quantity = parseInt(quantity_id.value)
        if (entered_quantity > parseInt(max_quantity)) {
            $("#quantity_span").addClass("text-danger");
            $("#submit-id-submit").prop("disabled", true);
        } else {
            $("#quantity_span").removeClass("text-danger");
            $("#submit-id-submit").prop("disabled", false);
        }
    });
}

function validate_quantity() {
    let quantity_id = document.getElementById("id_quantity");
    $("#id_plant").change(function () {
        quantity_id.value = "";
        document.getElementById("quantity_span").value = "";
        if (plant_source.value === "PITOMNIK") {
            show_quantity_and_change_button_property(quantity_id);
        } else {
            remove_quantity_validation();
        }
    });
}

function plant_source_action(plant_source, pitomnik_div, pitomnik_select, remove_flag=false) {
    if (plant_source.value === "PITOMNIK") {
        pitomnik_div.classList.remove("d-none");
        if (remove_flag){
            $("#id_plant option:not(:first)").remove();
        }
        plant_request(true);
    } else {
        pitomnik_div.classList.add("d-none")
        pitomnik_select.value = "";
        plant_request(false);
        remove_quantity_validation();
    }
}

$("#id_quantity").after(`<span id="quantity_span"></span>`);
let plant_source = document.getElementById("id_plant_source")
let pitomnik_div = document.getElementById("div_id_pitomnik")
let pitomnik_select = document.getElementById("id_pitomnik")
plant_source_action(plant_source, pitomnik_div, pitomnik_select);
validate_quantity();
plant_source.addEventListener("change", function (e) {
    plant_source_action(plant_source, pitomnik_div, pitomnik_select, true);
})