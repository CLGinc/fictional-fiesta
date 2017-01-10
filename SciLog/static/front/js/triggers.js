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
var removeInput = function(event) {
  $(event.target).closest('form').fadeOut(200, function() { $(this).remove(); });
};
$('[data-trigger="remove-input"]').click(function(){
	removeInput(event);
});
// add new input
$('[data-trigger="add-input"]').click(function(){
	var	currentId = $(this).attr('data-currentid'),
      newTargetId = 'email_input_'+(++currentId),
			targetForm =  $(this).attr('data-form'),
			sourceInput = document.getElementById(targetForm),
			cloneInput = sourceInput.cloneNode(true),
			insertTarget = $('#modal--participants').children('form').last(),
			upgradeTarget = $(cloneInput).children('div').get(0);
	$(upgradeTarget).removeClass('is-upgraded').removeAttr('data-upgraded').find('[name="email"]').val('');
  componentHandler.upgradeElement(upgradeTarget);
  $(cloneInput).attr('id',newTargetId).removeClass('hidden').hide().fadeIn(300).insertAfter(insertTarget);
	$(upgradeTarget).children('[data-trigger="remove-input"]').bind('click', removeInput);
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
  var targetForm = $('#modal--participants').children('form');
			$(targetForm).each(function(){
				var emailInput = $(this).find("input[name='email']"),
						url = $(this).attr('action');
				if($(emailInput).val()){
					var formData = $(this).serialize();
	        $.ajax({
	          url: url,
	          data: formData,
	          type: 'POST',
	          success: function(data)
	          {
	            console.log(data);
	          },
	          error: function(statusText,status,textStatus)
	          {
	            var errorNotif = textStatus;
							console.log(errorNotif);
	          },
	          complete: function(data)
	          {
	            // console.log(data);
	          }
	        });
				}
			});
  });
// $('[data-trigger="submit-ajax"]').click(function(){
//   var targetForm = '#'+$(this).attr('data-form'),
//       url = $(targetForm).attr('action'),
//       formData = $(targetForm).serialize();
// 			console.log(formData);
// 			$(targetForm).children('div').each(function(){
// 				var emailInput = $(this).children("input[name='email']");
// 				if(emailInput.val()){
// 	        $.ajax({
// 	          url: url,
// 	          data: formData,
// 	          type: 'POST',
// 	          success: function(data)
// 	          {
// 	            console.log(data);
// 	          },
// 	          error: function(statusText,status,textStatus)
// 	          {
// 	            var errorNotif = textStatus;
// 							// $(this).html('problem');
// 							console.log(errorNotif);
// 	          },
// 	          complete: function(data)
// 	          {
// 	            // console.log(data);
// 	          }
// 	        });
// 				}
// 			});
//   });
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
