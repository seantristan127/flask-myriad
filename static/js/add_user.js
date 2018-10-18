$(document).ready(function() {
	$('#submitUser').on('click', function() {
		$.ajax({
			data : {
			  fname : $('#fname').val(),
              lname : $('#lname').val(),
              email : $('#email').val(),
              password : $('#password').val()
			},
			type : 'POST',
			url : '/process_user'
		})
		.done(function(data) {

			$('#fname').val('');
			$('#lname').val('');
			$('#email').val('');
			$('#password').val('');


		});

		event.preventDefault();

	});

});