$('[data-trigger="addDataColumn"]').click(function() {
  $('[data-content="dataTable--parent"]').append(dataColumnTemplate);
  updateDataColumnOrder();
});

var updateDataColumnOrder = function(){
  var dataColumns = $('.dataTable--column');
  var index = 0;
  $(dataColumns).each(function(){
    $(this).attr('data-order', index);
    index++;
  });
};

var dataColumnTemplate = '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-3 dataTable--column" data-order="1"> <table class="mdl-data-table mdl-js-data-table mdl-shadow--2dp"><thead> <tr><div class="mdc-simple-menu table--menu dataColumn-1-menu" tabindex="-1" style="top:60px; right: 0; z-index:9999;"> <ul class="mdc-simple-menu__items mdc-list" role="menu" aria-hidden="true"><li class="mdc-list-item" role="menuitem" tabindex="0"> Copy data column</li><li class="mdc-list-item" role="menuitem" tabindex="0"> Edit</li><li class="mdc-list-item" role="menuitem" tabindex="0"> Delete</li></ul></div><th class="mdl-data-table__cell--non-numeric" colspan="2">Data</th><th><i class="material-icons list--link-options" data-trigger="table--menu" data-target="dataColumn-1-menu">more_vert</i></th> </tr></thead><tbody> <tr><td class="mdl-data-table__cell--non-numeric" colspan="2"> <input type="text" class="width--full"></td><td></td></tr></tbody><thead> <tr><th class="mdl-data-table__cell--non-numeric">Measurement</th><th class="mdl-data-table__cell--non-numeric">Unit</th><th class="mdl-data-table__cell--non-numeric"></th> </tr></thead><tbody> <tr><td class="mdl-data-table__cell--non-numeric"> <input type="text" class="width--full"></td><td class="mdl-data-table__cell--non-numeric"> <input type="text" class="width--full"></td><td></td></tr></tbody><thead> <tr><th class="mdl-data-table__cell--non-numeric" colspan="2">Resultset</th><th> <i class="material-icons list--link-add">add</i></th> </tr></thead><tbody> <tr><td class="mdl-data-table__cell--non-numeric" colspan="2"> <input type="text" class="width--full"></td><td> <i class="material-icons list--link-remove">clear</i></td></tr></tbody> </table></div>';
