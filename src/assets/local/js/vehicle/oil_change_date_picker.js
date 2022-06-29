let oil_change_hidden = $('#id_oil_change');
let oil_change_date_picker = $('#oil_change_date');
oil_change_date_picker.datepicker({format: 'yyyy-mm-dd'});
oil_change_date_datepiker = (element) => {
    oil_change_hidden.val(element.value);
}
oil_change_date_picker.val(oil_change_hidden.val());