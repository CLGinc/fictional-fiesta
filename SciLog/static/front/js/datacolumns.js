// function to add data row
$('[data-trigger="addDataRow"]').on('click', function() {
  var sourceElement = $('[data-content="table--row"]').last(),
      clonedElement = sourceElement.clone();
  clonedElement.find('input').each(function(){
    $(this).val('');
  });
  clonedElement.insertAfter(sourceElement);
});

// function to add data column
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

$('[data-trigger=submit-result]').click(function(){
  var independant = [],
      dataTableBuilder = [],
      independantValues = $('[data-content="independant-value"]'),
      independantTitle = $('[data-content="independant-title"]').val(),
      dataColumnsCount = $('[data-content="table--column"]').length,
      mainInput = $('[data-content="dataTable--input"]'),
      idependantData,
      dependantData,
      collectColumnData,
      dataTable;

  // collect values for independant data
  independantValues.each(function(){
    independant.push($(this).val());
  });

  // build independant data object and push it to the array
  idependantData = {data: independant, title: independantTitle, variable: 'independant'};
  dataTableBuilder.push(idependantData);

  // function to collect column data values
  collectColumnData = function(element){
    data.push($(this).children('input').val());
  };
  // iterate over dependant data columns, create objects and push them to the array
  for(currentCol = 0; currentCol < dataColumnsCount; currentCol++){
    var data = [],
        // index is +2 because column index starts from 1 and we ignore the first column
        index = currentCol + 2;
    var dependantValuesLocal = $('table').find('[data-type="dependant-value"]:nth-child('+index+')');

    $(dependantValuesLocal).each(collectColumnData);
    // dependantValuesLocal.each(collectDependantValues());
    dependantData = {data: data, title: $('[data-type="dependant-title"]').eq(currentCol).children('input').val(), variable: 'dependant'};
    dataTableBuilder.push(dependantData);
  }

  // generate final json
  dataTable = JSON.stringify({data_columns: dataTableBuilder});
  // set the json as value for the datatable input
  mainInput.val(dataTable);

  //submit form
  $('#create_protocol_result_form').submit();
});

// function to remove data row
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

// function to remove data column
$('[data-content="dataTable--parent"]').on('click', '[data-trigger="removeDataColumn"]', function() {
  var dataColumnsCount = $('[data-content="table--column"]').length;
  var parentColumn = $(this).closest('th, td').index();
  if(dataColumnsCount > 1){
    var target_tr = $('table tr').find('td:eq('+parentColumn+'),th:eq('+parentColumn+')');
    var saveTitle = $('table tr th').eq(1).html();
    $(target_tr).fadeOut("fast",function(){
        $(this).remove();
        if(parentColumn === 1){
          $('table tr th').eq(1).html(saveTitle);
        }
      });
    $('[data-content="table--column"]').first().remove();
  } else {
    var notif = 'At least one data column is required';
    show(snackbar,notif);
  }
});

// function to update variables from input value
$('[data-trigger="update-value"]').on('keyup', function(){
  var target = $(this).attr('data-target'),
      currentValue = $(this).val();
  $('#'+target).html(currentValue);
  if(currentValue.length === 0) {
    if(target === 'dependant-title') {
      $('#'+target).html('Dependant variable');
    } else if (target === 'independant-title') {
      $('#'+target).html('Independant variable');
    }
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
