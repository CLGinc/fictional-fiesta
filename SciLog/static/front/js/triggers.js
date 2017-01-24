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
      newTargetRole = newTargetId+'_role',
			targetForm =  $(this).attr('data-form'),
			sourceInput = document.getElementById(targetForm),
			cloneInput = $(sourceInput).clone(true),
			insertTarget = $('#modal--participants').children('form').last(),
			upgradeTarget = $(cloneInput);
      $(upgradeTarget).children().each(function () {
          $(this).removeClass('is-upgraded').removeAttr('data-upgraded').find('[name="email"]').val('');
      });
	// $(upgradeTarget).removeClass('is-upgraded').removeAttr('data-upgraded').find('[name="email"]').val('');
  componentHandler.upgradeElements(upgradeTarget);
  $(cloneInput).children('#email_input_source_role').attr('id',newTargetRole);
  $(cloneInput).children('[data-content="email_input_source_role"]').attr('data-content',newTargetRole);
  $(cloneInput).find('[for="email_input_source_role"]').attr('for',newTargetRole);
  $(cloneInput).attr('id',newTargetId).removeClass('hidden').hide().fadeIn(300).insertAfter(insertTarget);
	$(upgradeTarget).children('[data-trigger="remove-input"]').bind('click', removeInput);
	$(this).attr('data-currentid', currentId);
});
// selects
$('[data-trigger="selectValue"]').click(function(){
  var targetId = $(this).parent().attr('for'),
      targetInput = $('[data-content="'+targetId+'"]'),
      targetBtn = $('#'+targetId).children('[data-content="button--label"]'),
      selectValue = $(this).attr('data-value'),
      selectLabel = $(this).text();
  targetBtn.text(selectLabel);
  targetInput.val(selectValue);
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
					var currentForm = $(this),
							formData = currentForm.serialize(),
						 	loader = currentForm.find('div[data-content="loader"]'),
							button = currentForm.find('a[data-trigger="remove-input"]'),
							resultHolder = currentForm.children('div[data-content="result"]'),
							buttonIcon = button.children('i');
					button.toggleClass('hidden');
					loader.toggleClass('is-active');
	        $.ajax({
	          url: url,
	          data: formData,
	          type: 'POST',
	          success: function(response)
	          {
							resultHolder.html(response);
							loader.toggleClass('is-active');
							buttonIcon.html('check');
							button.toggleClass('hidden');
	          },
	          error: function(response)
	          {
              console.log(response);
	            var errorNotif = (jQuery.parseJSON(response.statusText)).email[0].message;
							resultHolder.html(errorNotif);
							loader.toggleClass('is-active');
							buttonIcon.html('close');
							button.toggleClass('hidden');
	          },
	          complete: function()
	          {
	            // anything to do here?
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
