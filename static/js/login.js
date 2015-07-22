$(document).ready(function(){
    initialize();
    buttonClicks();
});

function initialize(){
	$("#loginForm").hide();
	$("#registerForm").hide();
}

function buttonClicks(){
	$("#loginBtn").click(function(){
		$("#loginForm").slideDown();
		$("#registerForm").slideUp();
	});
	
	$("#registerBtn").click(function(){
		$("#registerForm").slideDown();
		//$("#loginForm").slideUp();
	});
}