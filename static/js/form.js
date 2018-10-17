$(document).ready(function(){
    $('#addUser').on('click', function() {

      $.ajax({
        data:{
          username : $('#username').val(),
          email : $('#email').val(),
          firstname : $('#firstname').val(),
          lastname : $('#lastname').val(),
          password : $('#password').val()
        },
        type : 'POST',
        url : '/admin_add_user'
      })
      .done(function(data) {

			$('#username').val('');
			$('#email').val('');
			$('#firstname').val('');
			$('#lastname').val('');
			$('#password').val('');
			$('#repeat-pass').val('');
		});
      event.preventDefault();
    });
});
