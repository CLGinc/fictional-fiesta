// Find checkbox state and toggle it
var toggleCheckbox = function(){
  var targetCheckbox = $(this).attr('data-target');
  if($('#'+targetCheckbox).prop('checked')){
    $('#'+targetCheckbox).prop('checked', false);
  } else {
    $('#'+targetCheckbox).prop('checked', true);
  }
};

// clean html after list is closed
var deleteOldList = function(requestTarget) {
  $('#'+requestTarget).empty();
};

// Ajax request to retrieve list
var addDataRequest = function(requestTarget) {
    // Configure the url we're about to hit
    $('[data-type="loader"]').removeClass('hidden');
    $('[data-type="loader"]').addClass('is-active');
    var dataTarget = requestTarget+'=True';
    $.ajax({
        url: viewParam,
        data: dataTarget,
        type: "GET",
        dataType: 'html',
        success: function(data) {
            // Append request template
    				$('#'+requestTarget).html(data);
            $('[data-trigger="checkbox"]').bind('click', toggleCheckbox);
        },
        error: function(data) {
            // When I get a 400 back, fail safely
            $('#'+requestTarget).html('There was a problem, please contact your administrator!');
        },
        complete: function(data){
            // Turn the scroll monitor back on
            // bind the event again so the user can open the list again
            $('[data-type="loader"]').addClass('hidden');
            $('[data-type="loader"]').removeClass('is-active');
        }
    });
};
