var editor;

$(document).ready(function(){
    initialize();
});

function initialize(){
	var language = document.getElementById("select_language");
	initiate_select_option(language.name);
	
	var config = {
		mode:  language.name,
		styleActiveLine: true,
		lineNumbers: true,
		indentWithTabs: true,
		tabSize: 4,
		theme: "eclipse",
		viewportMargin: Infinity
    };

    editor = CodeMirror.fromTextArea(document.getElementById("editor"), config);
	editor.setSize(500, 100);
	editor.refresh();
	
	set_autogrow();
}

function set_autogrow(){
	$("#prewords").autogrow();
	$("#afterwords").autogrow();
}



function initiate_select_option(language){
	var language_select = document.getElementById("select_language");
	for (var i=0; i<language_select.length; i++){
		if (language_select.options[i].value == language){
			language_select.options[i].selected = true;
		}
	}
}

function edit(article_id, article_type){
	var title = document.getElementById("title").value;

	if (article_type == "code snippet"){
		edit_code_snippet(article_id, title);
	}else if (article_type == "question"){
		edit_question(article_id, title);
	}else if (article_type == "findout"){
		edit_findout(article_id, title);
	}else{
		condole.log("Invalid article type");
	}
}

function edit_code_snippet(article_id, title){
	var language_input = document.getElementById("select_language");
    var language = language_input.options[language_input.selectedIndex].value;
    
    var prewords = document.getElementById("prewords").value;
    var afterwords = document.getElementById("afterwords").value;
    
    var form_data = {
    	id: article_id,
    	title: title,
    	code: editor.getValue(),
    	prewords: prewords,
    	afterwords: afterwords,
    	language: language
    }  
    
    $.ajax({
    	type: "post",
    	url: "/articles/code_snippet/save_changes",
    	data: JSON.stringify(form_data),
    	contentType: 'application/json;charset=UTF-8',
    	success: function(data){
    		var errorObj = $.parseJSON(data);
			if (!errorObj.iserror){
				window.location = "/articles/code_snippet/"+article_id;
			}else{
				console.log(errorObj.message);
			}
    	}
    });
}

function edit_question(article_id, title){
	var question = document.getElementById("question_text").value;

    var form_data = {
    	id: article_id,
    	title: title,
    	question: question
    }  
    
    console.log("question");
    
    $.ajax({
    	type: "post",
    	url: "/articles/question/save_changes",
    	data: JSON.stringify(form_data),
    	contentType: 'application/json;charset=UTF-8',
    	success: function(data){
    		var errorObj = $.parseJSON(data);
			if (!errorObj.iserror){
				window.location = "/articles/question/"+article_id;
			}else{
				console.log(errorObj.message);
			}
    	}
    });
}

function edit_findout(article_id, title){
	var findout = document.getElementById("findout_text").value;

    var form_data = {
    	id: article_id,
    	title: title,
    	findout: findout
    }  
    
    $.ajax({
    	type: "post",
    	url: "/articles/findout/save_changes",
    	data: JSON.stringify(form_data),
    	contentType: 'application/json;charset=UTF-8',
    	success: function(data){
    		var errorObj = $.parseJSON(data);
			if (!errorObj.iserror){
				window.location = "/articles/findout/"+article_id;
			}else{
				console.log(errorObj.message);
			}
    	}
    });
}
