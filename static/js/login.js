$(document).ready(function(){
    initialize();
    buttonClicks();
});

function initialize(){
	$("#login_window").hide();
	$("#register_window").hide();
}

function buttonClicks(){
	$("#loginBtn").click(function(){
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
	});
	$("#login").click(validate_login);
	
	$("#registerBtn").click(function(){
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
	});	
	$("#register").click(validate_registration);
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
	valid = valid && checkRegexp(passwd_obj,  /^([0-9a-zA-Z])+$/, error_field, invalid_passwd_msg);
	
	//send validation request to server to find out if username is unique
	
	return valid;
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
	
	//send  validation request to server
	
	return valid;
}


function checkLength(obj, name, min_len, max_len, error_field){
	if (obj.val().length > max_len || obj.val().length < min_len){
    	error_field.text("Length of "+name+" must be between "+min_len + " and "+max_len+".");
    	return false;
 	}
  	return true;
}

function checkRegexp(obj, regexp, error_field, error_msg){
 	if (!(regexp.test(obj.val()))) {
    	error_field.text(error_msg);
    	return false;
  	} else {
    	return true;
 	}
}

function comparePasswords(passwd, r_passwd, error_field, error_msg){
	if (passwd == r_passwd){
		return true;
	}	
 	error_field.text(error_msg);
	return false;
}
