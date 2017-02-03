// Datepicker init and variables
var toggleButtonFrom = document.getElementById('input-filter--date-from');
var toggleButtonTo = document.getElementById('input-filter--date-to');
var dialogFrom = new mdDateTimePicker.default({
  type: 'date',
  trigger: toggleButtonFrom
});
var dialogTo = new mdDateTimePicker.default({
  type: 'date',
  trigger: toggleButtonTo
});
// Datepicker events
//  From date
toggleButtonFrom.addEventListener('click', function() {
  dialogFrom.toggle();
});
toggleButtonFrom.addEventListener('onOk', function() {
  toggleButtonFrom.value = dialogFrom.time.format('YYYY-MM-DD').toString();
});
//  To date
toggleButtonTo.addEventListener('click', function() {
  dialogTo.toggle();
});
toggleButtonTo.addEventListener('onOk', function() {
  toggleButtonTo.value = dialogTo.time.format('YYYY-MM-DD').toString();
});
