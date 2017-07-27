(function(global) {
  [].forEach.call(document.querySelectorAll('.mdc-ripple-surface:not([data-demo-no-js])'), function(surface) {
    mdc.ripple.MDCRipple.attachTo(surface);
  });
})(this);
var MDCTemporaryDrawer = mdc.drawer.MDCTemporaryDrawer;
var drawer = new MDCTemporaryDrawer(document.querySelector('.mdc-temporary-drawer'));
document.querySelector('.menu').addEventListener('click', function() {
  drawer.open = !drawer.open;
});

// action button
$(window).load(function(){
  if($('.fixed-action-btn')){
    var actionButtons = $('.fixed-action-btn-list-action'),
        count = actionButtons.length,
        delayIndex = count,
        styleText = '';
    for (i=0; i<count; i++){
      delayIndex--;
      var childIndex = i + 1,
          delay = delayIndex * 30;
      styleText += '.fixed-action-btn-list.open li:nth-child('+childIndex+') .fixed-action-btn-list-action {-webkit-transition-delay: '+delay+'ms;transition-delay: '+delay+'ms;}';
    }
    $('head').append('<style>'+styleText+'</style>');
  }
});
$('.fixed-action-btn-main-btn a').mouseenter(function(){
  $('.fixed-action-btn-list').css("visibility", "visible").addClass('open');
  $('.fixed-action-btn-main-btn').addClass('edit');
});
$('[data-trigger="hover"]').mouseleave(function(){
  $('.fixed-action-btn-list').css("visibility", "hidden").removeClass('open');
  $('.fixed-action-btn-main-btn').removeClass('edit');
});
// scrolltop
$('.scrollToTop-button').click(function(){
	$('body,html').animate({scrollTop : 0},300);
});
// profile menu
$('[data-trigger="profile--menu"]').click(function() {
  var menuEl = document.querySelector('.profile--menu');
  var menu = new mdc.menu.MDCSimpleMenu(menuEl);
  menu.open = !menu.open;
});
$('#input--search').hover(function(){
  $(this).focus();
});
$('[data-trigger="open--search"]').on('click', function() {
  $('.toolbar__search-input').addClass('active');
  setTimeout(function(){
    $('#input--search').focus();
  },300);
});
$('[data-trigger="form--search"]').on('focusout', '#input--search',function() {
  $('.toolbar__search-input').removeClass('active');
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
    newButtonLabel = 'Update '+type;
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
// add new step trigger for protocol create
$('[data-trigger="add-step-create"]').click(function(event){
  addStepCreate();
});
// add new step trigger for protocol update
$('[data-trigger="add-step-edit"]').click(function(event){
  addStepEdit();
});
// main function to add steps in protocol create
var addStepCreate = function() {
  var clone;
  var sourceStep;
  addStepInit(event);
  addStepInsert();
  updateStepsCreate();
  addStepInitMDCelements();
  setNumberOfTotalForms();
  addStepCreateEvents();
  addStepEventsRemoveBtn();
};
// main function to add steps in protocol update
var addStepEdit = function() {
  var clone;
  var sourceStep;
  addStepInit(event);
  addStepEditOrder();
  addStepInsert();
  updateStepsEdit();
  addStepInitMDCelements();
  setNumberOfTotalForms();
  addStepEditEvents();
  addStepEventsRemoveBtn();
};
// add new step: find the source step, clone it and remvoe input values (visible)
var addStepInit = function(event){
	sourceStep =  event.target.parentElement.parentElement;
  var stepNumber = parseInt(sourceStep.getAttribute('data-step'));
	clone = sourceStep.cloneNode(true);
  $(clone).find('.mdc-textfield__label--float-above').removeClass('mdc-textfield__label--float-above');
  $(clone).find('.mdc-textfield__input').val('');
  $(clone).find('[data-content="form-id"]').remove();
  $(clone).find('[data-content="delete-step"]').remove();
};
// update name values for the new inserted step
var addStepEditOrder = function(){
  // the new step html order id is last so it does not override existing esteps
  var newStepOrder = $('.step').length;
  clone.querySelector('[data-content="step-title"]').setAttribute('name','steps-'+newStepOrder+'-title');
  clone.querySelector('[data-content="step-desc"]').setAttribute('name','steps-'+newStepOrder+'-text');
};
// add new step: insert the copied step
var addStepInsert = function(){
  $(clone).removeClass('hidden').insertAfter(sourceStep);
  $('html,body').animate({
    scrollTop: $(clone).offset().top}, 400);
};
// add new step: initialize the mdc elements
var addStepInitMDCelements = function(){
  window.mdc.autoInit(clone);
};
// add new step: add insert event listener for protocol create
var addStepCreateEvents = function(){
  clone.querySelector('[data-trigger="add-step-create"]').addEventListener('click', addStepCreate);
};
// add new step: add insert event listener for protocol update
var addStepEditEvents = function(){
  clone.querySelector('[data-trigger="add-step-edit"]').addEventListener('click', addStepEdit);
};
// add new step: add remove event listener
var addStepEventsRemoveBtn = function(){
  if(clone.querySelector('[data-trigger="remove-step"]')) {
    clone.querySelector('[data-trigger="remove-step"]').addEventListener('click', removeStep);
  } else if (clone.querySelector('[data-trigger="delete-step"]')) {
    clone.querySelector('[data-trigger="delete-step"]').addEventListener('click', removeStepEdit);
  }
};
// remove step
$('[data-trigger="remove-step"]').click(function(event){
  removeStep(event);
});
var removeStep = function(event){
  // do not execute the function if there is only 1 step
  if ($('.step').not('.hidden').length > 1){
    // find the container of the removed step
    var	sourceStep =  event.target.parentElement.parentElement;
    // remove the step
    $(sourceStep).remove();
    // update steps if needed
    if($(sourceStep).next()) {
      updateStepsCreate();
    }
    setNumberOfTotalForms(); // update number of total forms
  } else {
    // function is initialized only in the create protocol screen (inline)
    var notif = 'At least one step is required and step description is mandatory for all steps';
    show(snackbar,notif);
  }
};
// remove step edit: used in protocol update, when the step was added by the user and has not been submitted yet
var removeStepEdit = function(){
  if ($('.step').not('.hidden').length > 1){
    // find the container of the removed step
    var	sourceStep =  event.target.parentElement.parentElement;
    // remove the step
    $(sourceStep).remove();
    // update steps if needed
    if($(sourceStep).next()) {
      updateStepsEdit();
    }
    setNumberOfTotalForms(); // update number of total forms
  } else {
    // function is initialized only in the create protocol screen (inline)
    var notif = 'At least one step is required and step description is mandatory for all steps';
    show(snackbar,notif);
  }
};
// delete step: used in protocol update, when the step was loaded from database
$('[data-trigger="delete-step"]').click(function(event){
  deleteStep(event);
});
var deleteStep = function(event){
  // do not execute the function if there is only 1 step
  if ($('.step').not('.hidden').length > 1){
    var	sourceStep =  event.target.parentElement.parentElement;
    // mark the step for deletion and hide it from view
    $(sourceStep).children('[data-content="delete-step"]').prop('checked', true);
    $(sourceStep).addClass('hidden');
    updateStepsEdit(); // update step order
    setNumberOfTotalForms(); // update number of total forms
  } else {
    // function is initialized only in the create/edit protocol screens (inline)
    show(snackbar);
  }
};
// function to update steps during protocol create
var updateStepsCreate = function(){
  // find all steps to update and start counting from 0
  var steps = $('.step');
  var number = 0;
  // update each step according to their order
  $(steps).each(function(){
    var updateSteps = parseInt(this.getAttribute('data-step'));
    this.querySelector('[data-content="step-number"]').innerHTML = number+1;
    this.querySelector('[data-content="step-title"]').setAttribute('name','steps-'+number+'-title');
    this.querySelector('[data-content="step-desc"]').setAttribute('name','steps-'+number+'-text');
    this.setAttribute('data-step',number);
    number++;
  });
};
// function to update steps during protocol update
var updateStepsEdit = function(){
  // find all steps eligable for update (ignore deleted steps)
  var steps = $('.step').not('.hidden'),
      number = 0;
  // update each step order and display with the new value
  $(steps).each(function(){
    this.querySelector('[data-content="step-number"]').innerHTML = number+1; // display number is +1 of order
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

// submit form (standard submit)
$('[data-trigger="submit"]').click(function(){
  // targetelement is a target for an action before/after submit, usually the form container for closing e.t.c
  // target form is the form to submit
  var targetElementId = $(this).attr('data-target'),
      targetForm = $(this).attr('data-form');
  $('#'+targetForm).submit();
  if($('#'+targetElementId).hasClass('element--show-animate')){
    $('#'+targetElementId).removeClass('element--show-animate');
  }
  return false;
});

// submit setps form
$('[data-trigger="submitSteps"]').click(function(){
  // targetelement is a target for an action before/after submit, usually the form container for closing e.t.c
  // target form is the form to submit
  var targetElementId = $(this).attr('data-target'),
      targetForm = $(this).attr('data-form'),
      steps = $('[data-step]'),
      descInputs = $('[data-content="step-desc"]'),
      stepMain = $('[data-content="step-main"]'),
      data = [],
      stepsJson,
      isValid;

  descInputs.each(function() {
     if ($(this).val().trim() === '') {
      isValid = false;
     }
  });

  if(isValid === false) {
    var notif = 'At least one step is required and step description is mandatory for all steps';
    show(snackbar,notif);
  } else {
    steps.each(function(){
      data.push({'title': $(this).find('[data-content="step-title"]').val(), 'description' : $(this).find('[data-content="step-desc"]').val()});
    });
    stepsJson = JSON.stringify({'steps': data});
    stepMain.val(stepsJson);

    $('#'+targetForm).submit();
    if($('#'+targetElementId).hasClass('element--show-animate')){
      $('#'+targetElementId).removeClass('element--show-animate');
    }
    return false;
  }
});
// submit ajax invitations
$('[data-trigger="submit-ajax-invitation"]').click(function(){
  var targetForm = $(this).closest('form'),
      sendBtn = $(this),
      formData = targetForm.serialize(),
  		url = targetForm.attr('action'),
      loader = targetForm.find('div[data-content="loader"]'),
      button = targetForm.find('a'),
      parent = $(this).closest('[data-content="invitation-button"]');

      loader.toggleClass('is-active');
      $(sendBtn).addClass('hidden');

      $.ajax({
        url: url,
        data: formData,
        type: 'POST',
        success: function(response)
        {
          parent.html('<button class="mdc-button button--height-normal" disabled><p>Accepted</p></button>');
          loader.toggleClass('is-active');
        },
        error: function(response)
        {
          loader.toggleClass('is-active');
          button.html('<p>Try again</p>');
        },
        complete: function(response)
        {
          $(sendBtn).removeClass('hidden');
        }
      });
});

// submit ajax participants
$('[data-trigger="submit-ajax"]').click(function(){
  // store the target form and submit button element in vars
  var targetForm = $('#modal--participants').children('form');
  var sendBtn = this;
  // find all "email" inputs in the norm
	$(targetForm).each(function(){
		var emailInput = $(this).find("input[name='email']"),
				url = $(this).attr('action');
    // submit only if the input has value
		if($(emailInput).val()){
			var currentForm = $(this),
					formData = currentForm.serialize(),
				 	loader = currentForm.find('div[data-content="loader"]'),
					button = currentForm.find('a[data-trigger="remove-input"]'),
					resultHolder = currentForm.children('div[data-content="result"]'),
					buttonIcon = button.children('i');
      // some bling
			button.toggleClass('hidden');
			loader.toggleClass('is-active');
      $(sendBtn).addClass('disabled');
      $.ajax({
        url: url,
        data: formData,
        type: 'POST',
        success: function(json)
        {
          var name = '';
          if(json.invited_name){
            name = ' ('+json.invited_name+')';
          }
					resultHolder.removeClass('error').addClass('resultok').html('<p>Invitation to '+json.invited_email+name+' sent!</p>');
					loader.toggleClass('is-active');
					buttonIcon.html('check');
					button.toggleClass('hidden');
        },
        error: function(json)
        {
          var errorNotif = '';
          $.each((json.responseJSON), function() {
            errorNotif += '<p>'+this+'</p>';
          });
					resultHolder.removeClass('resultok').addClass('error').html(errorNotif);
					loader.toggleClass('is-active');
					buttonIcon.html('close');
					button.toggleClass('hidden');
        },
        complete: function(json)
        {
          $(sendBtn).removeClass('disabled');
        }
      });
		}
	});
});
