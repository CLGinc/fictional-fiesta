$('[data-trigger="addDataRow"]').on('click', function() {
  var sourceElement = $('[data-content="table--row"]').last();
  var clonedElement = sourceElement.clone();
  clonedElement.find('input').each(function(){
    $(this).val('');
  });
  clonedElement.insertAfter(sourceElement);
  updateColumnIndex();
});
$('[data-trigger="addDataColumn"]').on('click', function() {
  var sourceElement = $('[data-content="table--column"]').index(),
      colTemplate = '<col data-content="table--column"/>',
      empyThTemplate = '<th></th>',
      columnsCount = $('[data-content="table--column"]').length,
      lastColumnRemoveButton = $('[data-content="table--controls-remove_col"]').last();

  $('[data-content="table--column"]').last().after(colTemplate);
  $('[data-content="table--labels"]').append(empyThTemplate);
  $(removeColumnButton).insertAfter(lastColumnRemoveButton);
  $('table tbody tr').each(function() {
    var sourceTd = $(this).find('td:eq('+columnsCount+')'),
        clonedTd = sourceTd.clone();
    clonedTd.find('input').each(function(){
      $(this).val('');
    });
    $(clonedTd).insertAfter(sourceTd);
  });
});
var updateColumnIndex = function(){
  $('[data-index]').each(function(){
    console.log($(this));
    $(this).attr('data-index', $(this).index());
  });
};
$('[data-trigger=submit-result]').click(function(){
  var independant = [],
      independantValues = $('[data-content="independant-value"]'),
      independantTitle = $('[data-content="independant-title"]').val(),
      dataColumnsCount = $('[data-content="table--column"]').length;
  independantValues.each(function(){
    independant.push($(this).val());
  });
  var dependantData = {};
  for(currentCol = 0; currentCol < dataColumnsCount; currentCol++){
    dependantData = {title: $('[data-type="dependant-title"]').eq(currentCol).children('input').val()};
  }
  var idependantData = {data: independant, title: independantTitle, variable: 'independant'};
  // var dependantData =
  var data = [idependantData,dependantData];
  var dataTable = JSON.stringify({data_columns: data});
  console.log(dataTable);
});
var getColumnValues = function(){

};
$('[data-content="dataTable--parent"]').on('click', '[data-trigger="removeDataRow"]', function() {
  var dataRowsCount = $('[data-content="table--row"]').length;
  if(dataRowsCount > 1) {
  var parentRow = $(this).closest('tr');
  $(parentRow).fadeOut("fast",function(){
    $(this).remove();
  });
  } else {
    var notif = 'At least one data row is required';
    show(snackbar,notif);
  }
});
$('[data-content="dataTable--parent"]').on('click', '[data-trigger="removeDataColumn"]', function() {
  var dataColumnsCount = $('[data-content="table--column"]').length;
  var parentColumn = $(this).closest('th, td').index();
  if(dataColumnsCount > 1){
    var target_tr = $('table tr').find('td:eq('+parentColumn+'),th:eq('+parentColumn+')');
    $(target_tr).fadeOut("fast",function(){
        $(this).remove();
      });
    $('[data-content="table--column"]').first().remove();
  } else {
    var notif = 'At least one data column is required';
    show(snackbar,notif);
  }
});

// table highlights
$('table').on('mouseenter', 'th, td', function() {
  $(this).parents('table').find('col:eq('+$(this).index()+')').addClass('hover');
});
$('table').on('mouseleave', 'th, td', function() {
  $(this).parents('table').find('col:eq('+$(this).index()+')').removeClass('hover');
});

// templates
// remove col cell and button
var removeColumnButton = '<th data-content="table--controls-remove_col"> <div data-mdc-auto-init="MDCRipple" data-trigger="removeDataColumn" class="mdc-button table--button"> Remove col </div></th>';
