var MDCTemporaryDrawer = mdc.drawer.MDCTemporaryDrawer;
var drawer = new MDCTemporaryDrawer(document.querySelector('.mdc-temporary-drawer'));
document.querySelector('.menu').addEventListener('click', function() {
  drawer.open = !drawer.open;
});
// scrolltop
$('.scrollToTop-button').click(function(){
	$('body,html').animate({scrollTop : 0},300);
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
      type = $(button).attr('data-type'),
      buttons = document.getElementsByClassName('step__button'),
      newAction,
      newButtonLabel;
  if(action=='activate'){
    newAction = 'save';
    newButtonLabel = 'Save '+type;
  } else if (action=='save') {
    newAction = 'activate';
    newButtonLabel = 'Edit '+type;
    button.closest('form').submit();
  }
  $(button).attr('data-trigger', newAction).children('span').html(newButtonLabel);
  $(targets).each(function( i ) {
    $(this).attr('disabled', function (_, attr) { return !attr; }).parent().toggleClass('input--temp');
    $(this).toggleClass('textarea--temp');
  });
  $(buttons).each(function(){
    $(this).toggleClass('hidden');
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
  var lastForm = $(insertTarget).find('form').last();
  $(clone).removeClass('hidden').removeAttr('id').insertAfter(lastForm);
  clone.querySelector('[data-trigger="remove-input"]').addEventListener('click', removeInput);
	window.mdc.autoInit(clone);
});
// add new step
$('[data-trigger="add-step"]').click(function(event){
  addStep(event);
});
var addStep = function(event){
	var	sourceStep =  event.target.parentElement.parentElement,
      stepNumber = parseInt(sourceStep.getAttribute('data-step')),
			clone = sourceStep.cloneNode(true);
  stepNumber+=1;
  $(clone).find('.mdc-textfield__label--float-above').removeClass('mdc-textfield__label--float-above');
  $(clone).find('.mdc-textfield__input').val('');
  if(clone.querySelector('[data-content="form-id"]')) {
    clone.querySelector('[data-content="form-id"]').remove();
  }
  if(clone.querySelector('[data-content="delete-step"]')) {
    clone.querySelector('[data-content="delete-step"]').remove();
  }
  clone.querySelector('[data-content="step-input"]').setAttribute('value',stepNumber);
  clone.querySelector('[data-content="step-input"]').setAttribute('name','steps-'+stepNumber+'-order');
  clone.querySelector('[data-content="step-title"]').setAttribute('name','steps-'+stepNumber+'-title');
  clone.querySelector('[data-content="step-desc"]').setAttribute('name','steps-'+stepNumber+'-text');
  clone.setAttribute('data-step',stepNumber);
  stepNumber+=1;
  clone.querySelector('[data-content="step-number"]').innerHTML = stepNumber;
  var countNext = $(sourceStep).nextAll();
  if(countNext.length > 0) {
    $(countNext).each(function(){
      var updateSteps = parseInt(this.getAttribute('data-step'));
      updateSteps+=1;
      this.querySelector('[data-content="step-input"]').setAttribute('value',updateSteps);
      this.querySelector('[data-content="step-input"]').setAttribute('name','steps-'+updateSteps+'-order');
      this.querySelector('[data-content="step-title"]').setAttribute('name','steps-'+updateSteps+'-title');
      this.querySelector('[data-content="step-desc"]').setAttribute('name','steps-'+updateSteps+'-text');
      this.setAttribute('data-step',updateSteps);
      updateSteps+=1;
      this.querySelector('[data-content="step-number"]').innerHTML = updateSteps;
    }).not('.hidden');
  } else {
    $('body,html').animate({scrollTop : $('body').height()},300);
  }
  $(clone).removeClass('hidden').insertAfter(sourceStep);
  setNumberOfTotalForms();
  if(clone.querySelector('[data-trigger="remove-step"]')) {
    clone.querySelector('[data-trigger="remove-step"]').addEventListener('click', removeStep);
  } else if (clone.querySelector('[data-trigger="delete-step"]')) {
    clone.querySelector('[data-trigger="delete-step"]').addEventListener('click', removeStep);
  }
  clone.querySelector('[data-trigger="add-step"]').addEventListener('click', addStep);
	window.mdc.autoInit(clone);
};
// remove step
$('[data-trigger="remove-step"]').click(function(event){
  removeStep(event);
});
var removeStep = function(event){
  var steps = document.getElementsByClassName('step').length;
  if (steps > 1){
    var	sourceStep =  event.target.parentElement.parentElement,
        countNext = $(sourceStep).nextAll();
    if(countNext.length > 0) {
      $(countNext).each(function(){
        var updateSteps = parseInt(this.getAttribute('data-step'));
        this.querySelector('[data-content="step-number"]').innerHTML = updateSteps;
        updateSteps-=1;
        this.querySelector('[data-content="step-input"]').setAttribute('value',updateSteps);
        this.querySelector('[data-content="step-input"]').setAttribute('name','steps-'+updateSteps+'-order');
        this.querySelector('[data-content="step-title"]').setAttribute('name','steps-'+updateSteps+'-title');
        this.querySelector('[data-content="step-desc"]').setAttribute('name','steps-'+updateSteps+'-text');
        this.setAttribute('data-step',updateSteps);
      });
    }
    $(sourceStep).remove();
    setNumberOfTotalForms();
  } else {
    // function is initialized only in the create protocol screen (inline)
    show(snackbar);
  }
};
// delete step
$('[data-trigger="delete-step"]').click(function(event){
  deleteStep(event);
});
var deleteStep = function(event){
  var steps = $('.step').not('.hidden').length;
  if (steps > 1){
    var	sourceStep =  event.target.parentElement.parentElement,
        countNext = $(sourceStep).nextAll().not('.hidden');
    $(sourceStep).children('[data-content="delete-step"]').prop('checked', true);
    $(sourceStep).addClass('hidden');
    updateStepsEdit(sourceStep,countNext);
    setNumberOfTotalForms();
  } else {
    // function is initialized only in the create protocol screen (inline)
    show(snackbar);
  }
};
var updateStepsEdit = function(sourceStep,countNext){
  // find all steps eligable for update (ignore deleted steps)
  var steps = $('.step').not('.hidden'),
      number = 0;
  // update each step order and display with the new value
  $(steps).each(function(){
    this.querySelector('[data-content="step-number"]').innerHTML = number+1; // display number is +1 of order
    this.querySelector('[data-content="step-input"]').setAttribute('value',number);
    this.setAttribute('data-step',number);
    // increment number for next loop
    number++;
  });
};
// set number of total forms (steps)
var setNumberOfTotalForms = function(){
  var totalForms = $('.step').length;
  $('#id_steps-TOTAL_FORMS').val(totalForms);
};

// submit form
$('[data-trigger="submit"]').click(function(){
  var targetElementId = $(this).attr('data-target'),
      targetForm = $(this).attr('data-form');
  $('#'+targetForm).submit();
  $('#'+targetElementId).removeClass('element--show-animate');
  return false;
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
