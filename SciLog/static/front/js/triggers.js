// scrolltop
$('.scrollToTop-button').click(function(){
	$(win).animate({scrollTop : 0},300);
	return false;
});
// filters
$('[data-trigger="filter"]').click(function() {
  var targetElementId = $(this).attr('data-target');
  $('#'+targetElementId).slideToggle(200);
});
$('[data-trigger="filter-togglebtn"]').click(function() {
  var targetElementId = $(this).attr('data-target'),
      state = $(this).attr('data-state'),
      icon = $('[data-content="open-close-icon"]'),
      text = $('[data-content="open-close-text"]');
  $('#'+targetElementId).slideToggle(200);
  if(state === 'open'){
    icon.html('close');
    text.html('Cancel');
    $(this).attr('data-state','close');
  } else if (state === 'close'){
    icon.html('playlist_add');
    text.html('Add');
    $(this).attr('data-state','open');
  }
});
// expand
$('[data-trigger="expand"]').click(function() {
  var targetElementId = $(this).attr('data-target');
  $('#'+targetElementId).toggleClass('accordeon--expand');
});
// show
$('[data-trigger="show"]').click(function(){
  var targetElementId = $(this).attr('data-target');
  $('#'+targetElementId).toggleClass('element--show-animate');
});
$('[data-ajax="addDataRequest"]').click(function(){
  var targetElementId = $(this).attr('data-target'),
      requestTarget = $('#'+targetElementId).attr('data-request');
  addDataRequest(requestTarget);
});
// close
$('[data-trigger="close"]').click(function(){
  var targetElementId = $(this).attr('data-target'),
      requestTarget = $('#'+targetElementId).attr('data-request');
  $('#'+targetElementId).removeClass('element--show-animate');
  deleteOldList(requestTarget);
});
// add new input
$('[data-trigger="add-input"]').click(function(){
  var targetElementId = $(this).attr('data-target'),
			currentId = $(this).attr('data-currentid'),
      newTargetId = 'email_input_'+(++currentId),
			targetForm =  $(this).attr('data-form'),
			sourceInput = document.getElementById(targetElementId),
			cloneInput = sourceInput.cloneNode(true);
	$(cloneInput).removeClass('is-upgraded hidden').removeAttr('data-upgraded').attr('id',newTargetId).children('[name="email"]').val('');
  componentHandler.upgradeElement(cloneInput);
  $('#'+targetForm).append($(cloneInput).hide().fadeIn(200));
	$(this).attr('data-currentid', currentId);
});
// submit form
$('[data-trigger="submit"]').click(function(){
  var targetElementId = $(this).attr('data-target'),
      targetForm = $(this).attr('data-form');
  $('#'+targetElementId).removeClass('element--show-animate');
  $('#'+targetForm).submit();
});

$('[data-trigger="submit-ajax"]').click(function(){
  var targetForm = '#'+$(this).attr('data-form'),
      url = $(targetForm).attr('action'),
      formData = $(targetForm).serialize();
			$(targetForm).children('div').each(function(){
				var emailInput = $(this).children("input[name='email']");
				if(emailInput.val()){
	        $.ajax({
	          url: url,
	          data: formData,
	          type: 'POST',
	          success: function(data)
	          {
	            console.log(data);
	          },
	          error: function()
	          {
	            var errorNotif = '';
							$(targetForm).html('problem');
	          },
	          complete: function(data)
	          {
	            console.log(data);
	          }
	        });
				}
			});
  });
// update active tab and display add new button
$('[data-trigger="tab"]').click(function() {
  var activeTab = $(this).attr('data-target');
  if(activeTab=='none'){
    if(!$('#button-add').hasClass('hidden')){
      $('#button-add').addClass('hidden');
    }
  } else {
    if($('#button-add').hasClass('hidden')){
      $('#button-add').removeClass('hidden');
    }
  }
  $('#button-add').attr('data-target', activeTab);
});
