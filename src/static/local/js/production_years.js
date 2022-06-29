let id_organization = document.getElementById("id_organizations_choices")
let year = document.getElementById("id_years_choices")

function setYearlyProd() {
    let years_url = "/production/api/years/";
    let organization_id = id_organization.value
    let years = year.value
    $.ajax({
        url: years_url,
        data: {
            'year': years,
            'organization': organization_id
        },
        success: function (data) {
            $("#id_yearly_prod_plan").html(data);
        }
    });
}

setYearlyProd()
id_organization.addEventListener("change", function (e) {
    setYearlyProd();
})

year.addEventListener("change", function (e) {
    setYearlyProd();
})

