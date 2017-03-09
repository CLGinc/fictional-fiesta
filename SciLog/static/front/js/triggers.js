var MDCTemporaryDrawer = mdc.drawer.MDCTemporaryDrawer;
var drawer = new MDCTemporaryDrawer(document.querySelector('.mdc-temporary-drawer'));
document.querySelector('.menu').addEventListener('click', function() {
  drawer.open = !drawer.open;
});
// scrolltop
$('.scrollToTop-button').click(function(){
	$('body').animate({scrollTop : 0},300);
});
// profile menu
$('[data-trigger="profile--menu"]').click(function() {
  var menuEl = document.querySelector('.mdc-simple-menu');
  var menu = new mdc.menu.MDCSimpleMenu(menuEl);
  menu.open = !menu.open;
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
// activate
var editableInputs = function(button){
  var targetElementClass = $(button).attr('data-target'),
      targets = document.getElementsByClassName(targetElementClass),
      action = $(button).attr('data-trigger'),
      newAction,
      newButtonLabel;
  if(action=='activate'){
    newAction = 'save';
    newButtonLabel = 'Save project';
  } else if (action=='save') {
    newAction = 'activate';
    newButtonLabel = 'Edit project';
    button.closest('form').submit();
  }
  $(button).attr('data-trigger', newAction).children('span').html(newButtonLabel);
  $(targets).each(function( i ) {
    $(this).attr('disabled', function (_, attr) { return !attr; }).parent().toggleClass('input--temp');
  });
};
$('[data-trigger="activate"]').click(function(){
  button = $(this);
  editableInputs(button);
  return false;
});
$('[data-trigger="save"]').click(function(){
  button = $(this);
  editableInputs(button);
  return false;
});

// add data
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
	var	targetForm =  this.getAttribute('data-form'),
			sourceInput = document.getElementById(targetForm),
			clone = sourceInput.cloneNode(true);
			insertTarget = document.getElementById('modal--participants');
  var lastForm = $(insertTarget).children('form').last();
  $(clone).removeClass('hidden').removeAttr('id').hide().fadeIn(300).insertAfter(lastForm);
  clone.querySelector('[data-trigger="remove-input"]').addEventListener('click', removeInput);
	window.mdc.autoInit(clone);
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
  var sendBtn = this;
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
      $(sendBtn).addClass('disabled');
      $.ajax({
        url: url,
        data: formData,
        type: 'POST',
        success: function(response)
        {
					resultHolder.removeClass('error').addClass('resultok').html('<p>'+response+'</p>');
					loader.toggleClass('is-active');
					buttonIcon.html('check');
					button.toggleClass('hidden');
        },
        error: function(response)
        {
          var errorNotif = '';
          // test with multiple errors (replace response.statusText with json below)
          // var json = '{"__all__": [{"code": "unique_together", "message": "Invitation with this Email and Project already exists."}],"email":[{"code": "unique_together", "message": "mail not sent."}]}';
          $.each($.parseJSON(response.statusText), function() {
            errorNotif += '<p>'+this[0].message+'</p>';
          });
					resultHolder.removeClass('resultok').addClass('error').html(errorNotif);
					loader.toggleClass('is-active');
					buttonIcon.html('close');
					button.toggleClass('hidden');
        },
        complete: function(response)
        {
          $(sendBtn).removeClass('disabled');
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
