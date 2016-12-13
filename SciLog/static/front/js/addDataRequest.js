$(window).load(function(){
  addDataRequest();
});

var addDataRequest = function() {
    $('#loading').addClass('is-active');
    // Configure the url we're about to hit
    $.ajax({
        url: viewParam,
        data: {'protocols-to-add':'True'},
        type: "GET",
        dataType: 'html',
        success: function(data) {
            console.log(data);
            // Update global next page variable
    				$('#protocols_to_add_list').append(data);
        },
        error: function(data) {
            // When I get a 400 back, fail safely
            hasNextPage = false
        },
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            bindevent();
            $('#loading').removeClass('is-active');
        }
    });
};
