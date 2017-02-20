// Datepicker init and variables
var toggleButtonFrom = document.getElementById('input-filter--date-from'),
    toggleButtonFromLabel = $('#input-filter--date-from-label'),
    toggleButtonTo = document.getElementById('input-filter--date-to'),
    toggleButtonToLabel = $('#input-filter--date-to-label'),
    dialogFrom = new mdDateTimePicker.default({
  type: 'date',
  trigger: toggleButtonFrom
}),
  dialogTo = new mdDateTimePicker.default({
  type: 'date',
  trigger: toggleButtonTo
});
// Datepicker events
//  From date
toggleButtonFrom.addEventListener('click', function() {
  dialogFrom.toggle();
});
toggleButtonFrom.addEventListener('onOk', function() {
  if(!toggleButtonFromLabel.hasClass('mdc-textfield__label--float-above')){
    toggleButtonFromLabel.addClass('mdc-textfield__label--float-above');
  }
  toggleButtonFrom.value = dialogFrom.time.format('YYYY-MM-DD').toString();
});
//  To date
toggleButtonTo.addEventListener('click', function() {
  dialogTo.toggle();
});
toggleButtonTo.addEventListener('onOk', function() {
  if(!toggleButtonToLabel.hasClass('mdc-textfield__label--float-above')){
    toggleButtonToLabel.addClass('mdc-textfield__label--float-above');
  }
  toggleButtonTo.value = dialogTo.time.format('YYYY-MM-DD').toString();
});
