// // Events fired on window load (infinite scroll handling)
// $(window).load(function() {
// 	var win = $('main'),
//       totalPages = $('#total_pages').text(),
//       viewParam = $(location).attr('href');
//
//   //Click event to scroll to top
// 	$('.scrollToTop-button').click(function(){
// 		$(win).animate({scrollTop : 0},300);
// 		return false;
// 	});
//   // $('#paginator').addClass('hidden');
// 	// Each time the user scrolls
// 	$(win).scroll(function() {
// 		// End of the document reached?
//     var element = event.target;
// 		if(element.scrollHeight - element.scrollTop === element.clientHeight) {
//       var currentPage = parseInt($('#current_page_number').text()),
//           nextPageNumber = currentPage + 1,
//           newCurrentPage = nextPageNumber;
//       if(newCurrentPage <= totalPages) {
//   	    $('#loading').addClass('is-active');
//         $('#current_page_number').html(newCurrentPage);
//         console.log("ajax");
//       	$.ajax({
//               data: {
//                   page: nextPageNumber
//               },
//               type: "GET",
//         			url: viewParam,
//         			dataType: 'html',
//         			success: function(data) {
//                 var result = $('<li />').append(data).find('#items_list').html();
//         				$('#items_list').append(result);
//         				$('#loading').removeClass('is-active');
//       				}
//       			});
//         }
//   		}
// 	});
// });
$('.scrollToTop-button').click(function(){
	$(win).animate({scrollTop : 0},300);
	return false;
});

// Scroll globals
var pageNum = 1, // The latest page loaded
    hasNextPage = true, // Indicates whether to expect another page after this one
    viewParam = $(location).attr('href'),
    win = $('main');

$(window).load(function(){
  $(win).bind('scroll', loadOnScroll);
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
        dataType: 'json',
        success: function(data) {
            // Update global next page variable
            hasNextPage = true;//.hasNext;

            // Loop through all items
            for (i in data) {
                $("#items_list").after()
                console.log(data);
                // Do something with your json object response
            }
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
