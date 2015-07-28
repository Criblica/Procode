$(document).ready(function(){
    initialize();
});

function initialize(){
	$("#register_window").show();
	$('#register_window').jqxWindow({ 
		theme: "black", 
	 	width: "auto",
	 	height: "auto",
	 	minWidth: 300, 
	 	minHeight: 150,
	 	maxWidth: 350,
	 	maxHeight: 250, 
	 	isModal: true 
	});
	$('#register').jqxButton(function(){});	
	$("#register_window").on('close', function(){
		window.location="/";
	});
}

function validate_registration(){
	var valid = true;
	var uname_obj = $("#register_username");
	var passwd_obj = $("#register_password");
	var r_passwd_obj = $("#register_r_password");
	var error_field = $("#register_error");
	
	var invalid_username_msg = "Username may consist of a-z, A-Z, 0-9 and underscores.";
	var invalid_password_msg = "Password may consist of a-z, A-Z and 0-9";
	var non_equal_passwords_msg = "Passwords must be the same";
	
	valid = valid && checkLength(uname_obj, "username", 3, 16, error_field);
	valid = valid && checkLength(passwd_obj, "password", 6, 30, error_field);
	valid = valid && checkRegexp(uname_obj, /^([0-9a-zA-Z_])+$/i, error_field, invalid_username_msg);
	valid = valid && checkRegexp(passwd_obj,  /^([0-9a-zA-Z])+$/, error_field, invalid_password_msg);
	valid = valid && comparePasswords(passwd_obj.val(), r_passwd_obj.val(), error_field, non_equal_passwords_msg);
	
	if (valid){
		$.post(
			"/validate_registration",
			$("#registration_form").serialize(),
			function(data, status) {
				var errorObj = $.parseJSON(data);
				valid = valid && !errorObj.iserror;
				
				if (valid){
					error_field.text("");
					window.location = "/";
				}else{
					error_field.text(errorObj.message);
				}
			}
		);		
	}
}