$('#filter-button').click(function() {
  $('#filter-form').toggle(200);
});

$('#new-project-button').click(function() {
  $('#new-project-form').toggle(200);
});

// Datepicker init
var toggleButtonFrom = $('#input-filter--date-from'),
      dialogFrom = new mdDateTimePicker.default({
      type: 'date',
      trigger: document.getElementById("input-filter--date-from")
    }),
    labelFrom = $('#date-from--label');

toggleButtonFrom.click(function() {
  dialogFrom.toggle();
});

toggleButtonFrom.on('onOk', function() {
  dialogFrom.time = moment().format('YYYY-MM-DD');
  this.value = dialogFrom.time.toString();
  labelFrom.text(dialogFrom.time);
});
