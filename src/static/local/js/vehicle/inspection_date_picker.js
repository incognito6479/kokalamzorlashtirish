let inspection_date_hidden = $('#id_inspection');
let inspection_date_picker = $('#inspection_date');
inspection_date_picker.datepicker({format: 'yyyy-mm-dd'});
inspection_date_datepiker = (element) => {
    inspection_date_hidden.val(element.value);
}
inspection_date_picker.val(inspection_date_hidden.val());