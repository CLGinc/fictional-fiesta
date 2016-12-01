// scrolltop
$('.scrollToTop-button').click(function(){
	$(win).animate({scrollTop : 0},300);
	return false;
});
// accordeons
$('[data-trigger="expand"]').click(function() {
  var targetElementId = $(this).attr('data-target');
  console.log('click');
});
// filters
$('[data-trigger="filter"]').click(function() {
  var targetElementId = $(this).attr('data-target');
  $('#'+targetElementId).toggle(200);
});
