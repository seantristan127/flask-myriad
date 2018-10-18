
$(document).ready(function() {
	$('#book_id').on('click', function() {
	alert("Book added!")
		$.ajax({
			data : {
			  id : $('#book_id').val(),
			},
			type : 'POST',
			url : '/save_book'
		})
		.done(function(data) {
            alert("Book successfully added!")
		});
		event.preventDefault();
	});
});