$('#id_pitomnik').select2();
$('#id_plant').select2();
$('#id_plant__type').select2({minimumResultsForSearch: Infinity});
$('#id_status').select2({minimumResultsForSearch: Infinity});
let planted_date_hidden = $('#id_planted_date');
let readiness_date_hidden = $('#id_readiness_date');
let planted_date_picker = $('#planted_date');
let readiness_date_picker = $('#readiness_date');


planted_date_picker.datepicker({format: 'yyyy-mm-dd'});
readiness_date_picker.datepicker({format: 'yyyy-mm-dd'});

planted_date_datepiker = (element) => {
    planted_date_hidden.val(element.value);
}
readiness_date_datepiker = (element) => {
    readiness_date_hidden.val(element.value);
}
planted_date_picker.val(planted_date_hidden.val());
readiness_date_picker.val(readiness_date_hidden.val());