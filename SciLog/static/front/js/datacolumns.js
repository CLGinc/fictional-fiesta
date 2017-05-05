$('[data-trigger="addDataColumn"]').click(function() {
  $('[data-content="dataTable--parent"]').append(dataColumnTemplate);
  updateDataColumns();
});

var updateDataColumns = function(){
  var dataColumns = $('.dataTable--column'),
      index = 0;
  $(dataColumns).each(function(){
    $(this).attr('data-order', index);
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

var dataColumnTemplate = '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3 dataTable--column" data-order="0"> <table class="mdl-data-table mdl-js-data-table mdl-shadow--2dp"> <thead> <tr> <div class="mdc-simple-menu table--menu" data-content="dataColumn-0-menu" tabindex="-1" style="top:60px; right: 0; z-index:9999;"> <ul class="mdc-simple-menu__items mdc-list" role="menu" aria-hidden="true"> <li class="mdc-list-item" role="menuitem" tabindex="0"> Copy data column </li><li class="mdc-list-item" role="menuitem" tabindex="0"> Edit </li><li class="mdc-list-item" role="menuitem" tabindex="0"> Delete </li></ul> </div><th class="mdl-data-table__cell--non-numeric" colspan="2">Data</th> <th> <i class="material-icons list--link-options" data-trigger="table--menu" data-target="dataColumn-0-menu">more_vert</i> </th> </tr></thead> <tbody> <tr> <td class="mdl-data-table__cell--non-numeric" colspan="2"> <input type="text" class="width--full"> </td><td></td></tr></tbody> <thead> <tr> <th class="mdl-data-table__cell--non-numeric">Measurement</th> <th class="mdl-data-table__cell--non-numeric">Unit</th> <th class="mdl-data-table__cell--non-numeric">Independant</th> </tr></thead> <tbody> <tr> <td class="mdl-data-table__cell--non-numeric"> <input type="text" class="width--full"> </td><td class="mdl-data-table__cell--non-numeric"> <input type="text" class="width--full"> </td><td> <div class="mdc-checkbox center"> <input type="checkbox" class="mdc-checkbox__native-control"/> <div class="mdc-checkbox__background"> <svg class="mdc-checkbox__checkmark" viewBox="0 0 24 24"> <path class="mdc-checkbox__checkmark__path" fill="none" stroke="white" d="M1.73,12.91 8.1,19.28 22.79,4.59"/> </svg> <div class="mdc-checkbox__mixedmark"></div></div></div></td></tr></tbody> <thead> <tr> <th class="mdl-data-table__cell--non-numeric" colspan="2">Resultset</th> <th> remove / add </th> </tr></thead> <tbody> <tr> <td class="mdl-data-table__cell--non-numeric" colspan="2"> <input type="text" class="width--full"> </td><td> <i class="material-icons list--link-remove" data-trigger="remove--datarow" data-mdc-auto-init="MDCRipple">clear</i> <i class="material-icons list--link-add" data-trigger="add--datarow">add</li></td></tr></tbody> </table> </div>';

var dataRowTemplate = '<tr><td class="mdl-data-table__cell--non-numeric" colspan="2"> <input type="text" class="width--full"> </td><td> <i class="material-icons list--link-remove" data-trigger="remove--datarow">clear</i> <i class="material-icons list--link-add" data-trigger="add--datarow">add</li></td></tr>';
