$(document).ready(function(){
    initialize();
    buttonClicks();
});

function initialize(){
	dialog = $("#login_dialog").dialog({
		autoOpen:false,
		height: 300,
		width: 350,
		modal: true,
		buttons: {
			"Cancel": cancel,
			Cancel: function(){
				dialog.dialog("close");
			}
		},
		close: function(){
			form[0].reset();
		}
	});
}

function buttonClicks(){
	$("#loginBtn").click(function(){
		dialog.dialog("open");
	});
	
	$("#registerBtn").click(function(){
		
	});
}
