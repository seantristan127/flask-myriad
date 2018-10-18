
$(document).ready(function() {
	$('#submitBook').on('click', function() {
		$.ajax({
			data : {
			  name : $('#book_name').val(),
              description : $('#description').val(),
              genre : $('#author').val(),
              isbn : $('#isbn').val(),
              author : $('#type').val()
			},
			type : 'POST',
			url : '/upload_book'
		})
		.done(function(data) {

            alert("Book successfully added!")
			$('#book_name').val('');
			$('#description').val('');
			$('#author').val('');
			$('#isbn').val('');
			$('#type').val('');


		});

		event.preventDefault();

	});

});