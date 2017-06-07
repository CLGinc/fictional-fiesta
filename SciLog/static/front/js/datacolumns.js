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

// submit result
$('[data-trigger=submit-result]').click(function(){
  var dependent = [],
      independent = [],
      independentData = [],
      independentValues = $('[data-type="independent-value"]'),
      independentTitle = $('[data-content="independent-title"]').val(),
      dataColumnsCount = $('[data-content="table--column"]').length,
      mainInput = $('[data-content="dataTable--input"]'),
      collectColumnData,
      dataTable;

  // collect values for independent data
  independentValues.each(function(){
    var dataType = $('[data-target="independent-value"]').val();
    if(dataType === 'boolean') {
      independentData.push($(this).find('input').prop("checked"));
    } else if(dataType === 'number') {
      value = Number.parseFloat($(this).find('input').val());
      independentData.push(value);
    } else {
      independentData.push($(this).find('input').val());
    }
  });

  // build independent data object and push it to the array
  independent.push({data: independentData, title: independentTitle});
  // dataTableBuilder.push(idependentData);

  // function to collect column data values
  collectColumnData = function(element){
    var dataType = $('[data-target="dependent-value"]').val();
    if(dataType === 'boolean') {
      data.push($(this).find('input').prop("checked"));
    } else if(dataType === 'number') {
      value = Number.parseFloat($(this).find('input').val());
      data.push(value);
    } else {
      data.push($(this).find('input').val());
    }
  };

  // iterate over dependent data columns, create objects and push them to the array
  for(currentCol = 0; currentCol < dataColumnsCount; currentCol++){
    var data = [],
        // index is +2 because column index starts from 1 and we ignore the first column
        index = currentCol + 2;
    var dependentValuesLocal = $('table').find('[data-type="dependent-value"]:nth-child('+index+')');

    $(dependentValuesLocal).each(collectColumnData);
    // dependentValuesLocal.each(collectdependentValues());
    dependent.push({data: data, title: $('[data-type="dependent-title"]').eq(currentCol).children('input').val()});
  }
  // dataTableBuilder.push(dependent);

  // generate final json
  dataTable = JSON.stringify({data_columns: {'independent_variable': independent,'dependent_variable': dependent}});
  // set the json as value for the datatable input
  mainInput.val(dataTable);
  console.log(dataTable);

  //submit form
  // $('#create_protocol_result_form').submit();
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
    if(target === 'dependent-title') {
      $('#'+target).html('dependent variable');
    } else if (target === 'independent-title') {
      $('#'+target).html('Independent variable');
    }
  }
});

// Update inputs with correct data type
$('[data-trigger="data-type"]').on('change', function(e){
  var newDataType = $(this).val(),
      targetVariable = $(this).data('target'),
      parents = $('[data-type="'+targetVariable+'"]');
  if(newDataType === 'number'){
    parents.empty().append(inputTemplateNumber);
  } else if(newDataType === 'string') {
    parents.empty().append(inputTemplateString);
  } else if(newDataType === 'boolean') {
    parents.empty().append(checkboxTemplate);
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
// checkbox before input
var inputTemplateString = '<input type="text" placeholder="Add value" class="text-right dataTypeInput">';
var inputTemplateNumber = '<input type="number" placeholder="Add value" class="text-right dataTypeInput">';
// checkbox after input
var checkboxTemplate = '<div class="mdc-checkbox"> <input type="checkbox" class="mdc-checkbox__native-control dataTypeInput"/> <div class="mdc-checkbox__background"> <svg class="mdc-checkbox__checkmark" viewBox="0 0 24 24"> <path class="mdc-checkbox__checkmark__path" fill="none" stroke="white" d="M1.73,12.91 8.1,19.28 22.79,4.59"/> </svg> <div class="mdc-checkbox__mixedmark"></div></div></div>';
// remove col cell and button
var removeColumnButton = '<th data-content="table--controls-remove_col"> <div data-mdc-auto-init="MDCRipple" data-trigger="removeDataColumn" class="mdc-button table--button"> Remove col </div></th>';
