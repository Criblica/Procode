function post_comment(article_id, article_type){
	var error_field = $("#error_msg");
	var comment_field = document.getElementById("post_comment_text");
	
	if (comment_field.value == ""){
		error_field.text("Cannot post empty comment.");
		return;
	}
	
	var data = {
		message: comment_field.value,
		article_id: article_id,
		article_type: article_type
	}
	
	$.ajax({
		type: "post",
		url: "/articles/post_comment",
		data: JSON.stringify(data),
		contentType: 'application/json;charset=UTF-8',
		success: function(data){
			var errorObj = $.parseJSON(data);
			if (!errorObj.iserror){
				error_field.text("");
				location.reload();
			} else{
				error_field.text(errorObj.message);
			}
		}	
	});
}