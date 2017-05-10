$('[data-trigger="addDataColumn"]').click(function() {
  $('[data-content="dataTable--parent"]').append(dataColumnTemplate);
  updateDataColumns();
});
$('[data-content="dataTable--parent"]').on('click', '[data-trigger="remove-table"]', function() {
  if($('.dataTable--column').length > 1){
	   $(event.target).closest('.dataTable--column').fadeOut(200, function() {
       $(this).remove();
       updateDataColumns();
     });
  }
});

var updateDataColumns = function(){
  var dataColumns = $('.dataTable--column'),
      prefix = 'data_columns-',
      totalForms = dataColumns.length,
      index = 0;
  $('#id_data_columns-TOTAL_FORMS').val(totalForms);
  $(dataColumns).each(function(){
    $(this).attr('data-order', index);
    $(this).children('[data-content="order"]').attr('name', prefix+index+'-order');
    $(this).children('[data-content="data-merged"]').attr('name', prefix+index+'-data');
    $(this).find('[data-content="label"]').attr('name', prefix+index+'-label');
    $(this).find('[data-content="measurement"]').attr('name', prefix+index+'-measurement');
    $(this).find('[data-content="unit"]').attr('name', prefix+index+'-unit');
    $(this).find('.table--menu').attr('data-content', 'dataColumn-'+index+'-menu');
    $(this).find('[data-trigger="table--menu"]').attr('data-target', 'dataColumn-'+index+'-menu');
    index++;
  });
};

// table menu
$('[data-content="dataTable--parent"]').on('click', '[data-trigger="table--menu"]', function() {
  var target = $(event.target).attr('data-target'),
      menuEl = document.querySelector('[data-content="'+target+'"]'),
      menu = new mdc.menu.MDCSimpleMenu(menuEl);
  menu.open = !menu.open;
});
$('[data-content="dataTable--parent"]').on('click', '[data-trigger="remove--datarow"]', function() {
  var dataRows = $(event.target).closest('tbody').children().length;
  if(dataRows > 1){
    $(event.target).closest('tr').remove();
  }
});
$('[data-content="dataTable--parent"]').on('click', '[data-trigger="add--datarow"]', function() {
  $(event.target).closest('tbody').append(dataRowTemplate);
});

var dataColumnTemplate = '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3 dataTable--column" data-order="0"> <input type="text" name="data_columns-0-order" value="0" data-content="order" class="hidden"> <input type="text" name="data_columns-0-data" value="0" data-content="data-merged" class="hidden"> <table class="mdl-data-table mdl-js-data-table mdl-shadow--2dp"> <thead> <tr> <th class="mdl-data-table__cell--non-numeric" colspan="2">Label</th> <th> <i class="material-icons list--link-remove" data-trigger="remove-table">clear</i> </th> </tr></thead> <tbody> <tr> <td class="mdl-data-table__cell--non-numeric" colspan="3"> <input type="text" class="width--full" name="data_columns-0-label" data-content="label"> </td></tr></tbody> <thead> <tr> <th class="mdl-data-table__cell--non-numeric" colspan="2">Measurement</th> <th class="mdl-data-table__cell--non-numeric">Unit</th> </tr></thead> <tbody> <tr> <td class="mdl-data-table__cell--non-numeric" colspan="2"> <input type="text" class="width--full" name="data_columns-0-measurement" data-content="measurement"> </td><td class="mdl-data-table__cell--non-numeric"> <input type="text" class="width--full" name="data_columns-0-unit" data-content="unit"> </td></tr></tbody> <thead> <tr> <th class="mdl-data-table__cell--non-numeric" colspan="2">Data</th> <th> remove / add </th> </tr></thead> <tbody> <tr> <td class="mdl-data-table__cell--non-numeric" colspan="2"> <input type="text" class="width--full" data-content="data"> </td><td> <i class="material-icons list--link-remove" data-trigger="remove--datarow" data-mdc-auto-init="MDCRipple">clear</i> <i class="material-icons list--link-add" data-trigger="add--datarow">add</li></td></tr></tbody> </table> </div>';

var dataRowTemplate = '<tr> <td class="mdl-data-table__cell--non-numeric" colspan="2"> <input type="text" class="width--full" data-content="data"> </td><td> <i class="material-icons list--link-remove" data-trigger="remove--datarow" data-mdc-auto-init="MDCRipple">clear</i> <i class="material-icons list--link-add" data-trigger="add--datarow">add</li></td></tr>';
