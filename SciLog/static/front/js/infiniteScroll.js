// Events fired on window load (infinite scroll handling)
$(window).load(function() {
	var win = $('main'),
      totalPages = $('#total_pages').text(),
      viewParam = $(location).attr('href');

  //Click event to scroll to top
	$('.scrollToTop-button').click(function(){
		$(win).animate({scrollTop : 0},300);
		return false;
	});
  $('#paginator').addClass('hidden');
	// Each time the user scrolls
	$(win).scroll(function() {
		// End of the document reached?
    var element = event.target;
		if(element.scrollHeight - element.scrollTop === element.clientHeight) {
      var currentPage = parseInt($('#current_page_number').text()),
          nextPageNumber = currentPage + 1,
          newCurrentPage = nextPageNumber,
          pageBaseLink = $('#paginator_next').attr('href')
          newNextPageLink = "?page="+(nextPageNumber+1);
      if(newCurrentPage <= totalPages) {
  	    $('#loading').addClass('is-active');
        $('#current_page_number').html(newCurrentPage);
        $('#paginator_next').attr('href', newNextPageLink);

    		$.ajax({
          data: {
                txtsearch: $('#items_list').val()
            },
          type: "GET",
    			url: viewParam + '?page=' + nextPageNumber,
    			dataType: 'html',
    			success: function(data) {
            var result = $('<tbody />').append(data).find('#items_list').html();
    				$('#items_list').append(result);
    				$('#loading').removeClass('is-active');
    				}
    			});
        }
  		}
	});
});
