$(document).ready(function(){
    initialize();
});

function initialize(){
	$("#login_window").show();
 	$('#login_window').jqxWindow({ 
		theme: "black", 
		width: "auto",
		height: "auto",
		minWidth: 280, 
		minHeight: 150,
		maxWidth: 350,
		maxHeight: 200,
		isModal: true
	});
	$('#login').jqxButton(function(){});
	$("#login_window").on('close', function(){
		window.location="/";
	});
}

function validate_login(){
	var valid = true;
	var uname_obj = $("#login_username");
	var passwd_obj = $("#login_password");
	var error_field =  $("#login_error");
	
	var invalid_username_msg = "Username may consist of a-z, A-Z, 0-9 and underscores.";
	var invalid_password_msg = "Password may consist of a-z, A-Z and 0-9";
	
	valid = valid && checkLength(uname_obj, "username", 3, 16, error_field);
	valid = valid && checkLength(passwd_obj, "password", 6, 30, error_field);
	valid = valid && checkRegexp(uname_obj, /^([0-9a-zA-Z_])+$/i, error_field, invalid_username_msg);
	valid = valid && checkRegexp(passwd_obj,  /^([0-9a-zA-Z])+$/, error_field, invalid_password_msg);
	
	if (valid){
		$.post(
			"/validate_login",
			$("#login_form").serialize(),
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
