$(window).load(function(){
  addDataRequest();
});
// Find checkbox state and toggle it
var toggleCheckbox = function(){
  var targetCheckbox = $(this).attr('data-target');
  if($('#'+targetCheckbox).prop('checked')){
    $('#'+targetCheckbox).prop('checked', false);
  } else {
    $('#'+targetCheckbox).prop('checked', true);
  }
};
// Ajax request to retrieve list
var addDataRequest = function() {
    $('#loading').addClass('is-active');
    // Configure the url we're about to hit
    $.ajax({
        url: viewParam,
        data: {'protocols-to-add':'True'},
        type: "GET",
        dataType: 'html',
        success: function(data) {
            // Update global next page variable
    				$('#protocols_to_add_list').append(data);
            $('[data-trigger="checkbox"]').bind('click', toggleCheckbox);
        },
        error: function(data) {
            // When I get a 400 back, fail safely
            // bind a new event to the add button so the user can retry
        },
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            // bind the event again so the user can open the list again
            $('#loading').removeClass('is-active');
        }
    });
};
