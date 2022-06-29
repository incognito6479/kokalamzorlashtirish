let months_id = document.getElementById("id_months");
let years_id = document.getElementById("id_year");

function setMonthlyPlan() {
    let years = years_id.value
    let months = months_id.value
    let months_url = "/production/api/months/";

    $.ajax({
        url: months_url,
        data: {
            'year': years,
            'month': months
        },
        success: function (data) {
            $("#id_monthly_prod_plan").html(data);
        }
    });
}

setMonthlyPlan()
months_id.addEventListener("change", function (e) {
    setMonthlyPlan();
})

