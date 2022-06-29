let manufactured_date_hidden = $('#id_manufactured_date');
let manufactured_date_picker = $('#manufactured_date');
manufactured_date_picker.datepicker({format: 'yyyy-mm-dd'});
manufactured_date_datepiker = (element) => {
    manufactured_date_hidden.val(element.value);
}
manufactured_date_picker.val(manufactured_date_hidden.val());