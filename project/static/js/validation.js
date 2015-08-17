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