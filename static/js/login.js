$(document).ready(function(){
    initialize();
    buttonClicks();
});

function initialize(){
	
	
}

function buttonClicks(){
	$("#loginBtn").click(function(){
		 //$( "#login_dialog" ).dialog();
		 $('#login_dialog').jqxWindow({ theme: "shinyblack", width: 250, height: 130, isModal: true });
        $('#submit').jqxButton({ theme: "shinyblack" });
	});
	
	$("#registerBtn").click(function(){
		
	});
}
