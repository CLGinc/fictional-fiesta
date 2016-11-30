$('.scrollToTop-button').click(function(){
	$(win).animate({scrollTop : 0},300);
	return false;
});

// Scroll globals
var pageNum = 1, // The latest page loaded
    hasNextPage = true, // Indicates whether to expect another page after this one
    viewParam = $(location).attr('href'),
    datamode = $('#items_list').attr('data-mode'),
    win = $('main');
    loadmorebtn = $("#loadmorebtn")

$(window).load(function(){
  if(datamode == 'infinitescroll'){
    $(win).bind('scroll', loadOnScroll);
    alert('infinitescroll');
  } else if(datamode == 'loadmore') {
    alert('loadmore');
  }
  return false;
});

// loadOnScroll handler
var loadOnScroll = function() {
   // If the current scroll position is past out cutoff point...
    var element = event.target;
        if(element.scrollHeight - element.scrollTop === element.clientHeight) {
        // temporarily unhook the scroll event watcher so we don't call a bunch of times in a row
        $(win).unbind();
        // execute the load function below that will visit the JSON feed and stuff data into the HTML
        loadItems();
    }
};

var loadItems = function() {
    $('#loading').addClass('is-active');
    // If the next page doesn't exist, just quit now
    if (hasNextPage === false) {
        console.log('nonext');
        $('#loading').removeClass('is-active');
        return false
    }
    // Update the page number
    pageNum = pageNum + 1;
    console.log(pageNum+' '+viewParam+' '+hasNextPage);
    // Configure the url we're about to hit
    $.ajax({
        url: viewParam,
        data: {page: pageNum},
        type: "GET",
        dataType: 'html',
        success: function(data) {
            // Update global next page variable
            hasNextPage = true;//.hasNext;
            var result = $('<li />').append(data).find('#items_list').html();
    				$('#items_list').append(result);
        },
        error: function(data) {
            // When I get a 400 back, fail safely
            hasNextPage = false
        },
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            $(win).bind('scroll', loadOnScroll);
            $('#loading').removeClass('is-active');
        }
    });
};
