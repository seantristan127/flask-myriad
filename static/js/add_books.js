
$(document).ready(function() {
	$('#submitBook').on('click', function() {
		$.ajax({
			data : {
			  name : $('#name').val(),
              description : $('#description').val(),
              genre : $('#genre').val(),
              image_link : $('#image_link').val(),
              author : $('#author').val()
			},
			type : 'POST',
			url : '/upload_book'
		})
		.done(function(data) {

			$('#name').val('');
			$('#description').val('');
			$('#genre').val('');
			$('#image_link').val('');
			$('#author').val('');


		});

		event.preventDefault();

	});

});