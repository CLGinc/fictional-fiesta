// scrolltop
$('.scrollToTop-button').click(function(){
	$(win).animate({scrollTop : 0},300);
	return false;
});
// accordeons
// $('#accordeon--protocols').hide();
// $('[data-trigger="expand"]').click(function() {
//   var targetElementId = $(this).attr('data-target');
//   $('#'+targetElementId).toggle();
//   console.log('click');
// });
$('#accordeon--protocols').readmore({
  speed: 300,
  moreLink: '<div class="mdl-card__actions"><a class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-color-text--blue-grey-600"><i class="material-icons mdl-color-text--blue-500">expand_more</i>See all protocols</a></div>',
  lessLink: '<div class="mdl-card__actions"><a class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-color-text--blue-grey-600"><i class="material-icons mdl-color-text--blue-500">expand_more</i>See all protocols</a></div>'
});
// filters
$('[data-trigger="filter"]').click(function() {
  var targetElementId = $(this).attr('data-target');
  $('#'+targetElementId).toggle(200);
});
