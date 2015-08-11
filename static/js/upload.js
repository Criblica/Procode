$(document).ready(function(){
    initialize();
});

function initialize(){
	$("#upload_window").show();
 	$('#upload_window').jqxWindow({ 
		theme: "black", 
		/*width: "auto",
		height: "auto",
		minWidth: 280, 
		minHeight: 150,
		maxWidth: 700,
		maxHeight: 500,*/
		width: 500,
		height: 380,
		isModal: true
	});
	$("#upload_window").on('close', function(){
		window.location="/";
	});
	
	$("#hidden_area").hide();
    
    $("#upfile").change(function() {
    	readURL(this);
	});
	
	/*document.getElementById('upload_form').onsubmit = function() {
	    return validate();
	}*/
	
}

function switch_image(src){
	$("#chosen_image").attr('src', src);
}

function readURL(input){
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
        	console.log(e.target.result);
            $('#chosen_image').attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function choose_image(){
	$("#upfile").click();
}

function validate(){
	$('.thumbnail').each(function(i, obj) {
	    if (obj.src == $("#chosen_image").attr('src')){
	    	var data = {image_src: obj.src}
	    
			$.ajax({
				type: "post",
				url: "/use_image",
				async: false,
				data: JSON.stringify(data),
				contentType: 'application/json;charset=UTF-8',
				success: function(data, status) {
					var errorObj = $.parseJSON(data);
					if (!errorObj.iserror){
						window.location = "/";
					}else{
						console.log(errorObj.message);
					}
					return false;
				}
			});	
			
		}else{
			return true;
		}
	});
}