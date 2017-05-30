$('[data-trigger="addDataRow"]').on('click', function() {
  var sourceElement = $('[data-content="table--row"]').last();
  var clonedElement = sourceElement.clone();
  clonedElement.find('input').each(function(){
    $(this).val('');
  });
  clonedElement.insertAfter(sourceElement);
});
$('[data-trigger="addDataColumn"]').on('click', function() {
  var sourceElement = $('[data-content="table--column"]').index(),
      colTemplate = '<col data-content="table--column"/>',
      empyThTemplate = '<th></th>';

  $('[data-content="table--dependant-variable"]').append(empyThTemplate);
  $('[data-content="table--column"]').last().after(colTemplate);
  $('table tr').each(function(index) {
    $('[data-content="table--row"]').append($("<td contenteditable='true'></td>"));
  });
});
$('[data-content="dataTable--parent"]').on('click', '[data-trigger="removeDataRow"]', function() {
  var dataRowsCount = $('[data-content="table--row"]').length;
  if(dataRowsCount > 1) {
  var parentRow = $(this).closest('tr');
  parentRow.remove();
  } else {
    var notif = 'At least one data row is required';
    show(snackbar,notif);
  }
});
$('[data-content="dataTable--parent"]').on('click', '[data-trigger="removeDataColumn"]', function() {
  var dataColumnsCount = $('[data-content="table--column"]').length;
  var parentColumn = $(this).index();
  console.log(parentColumn);
  if(dataColumnsCount > 1){
    var target_tr = $('table tr').find('td:eq('+parentColumn+'),th:eq('+parentColumn+')');
    $(target_tr).fadeOut("fast",function(){
        $(this).remove();
      });
  } else {
    var notif = 'At least one data column is required';
    show(snackbar,notif);
  }
});

$('th, td').hover(function() {
 $(this).parents('table').find('col:eq('+$(this).index()+')').toggleClass('hover');
});
