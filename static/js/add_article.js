var editor;

$(document).ready(function(){
    initialize();
});

function initialize(){
	type_selection();
	
	document.getElementById("select_type").onchange = function(){
		type_selection();
	};
		
	var config = {
		mode:  "python",
		styleActiveLine: true,
		lineNumbers: true,
		indentWithTabs: true,
		tabSize: 4,
		theme: "eclipse",
		viewportMargin: Infinity
    };

    editor = CodeMirror.fromTextArea(document.getElementById("editor"), config);
	editor.setSize(500, 100);
}

function selectLanguage(){
	var language_input = document.getElementById("select_language");
	var language = language_input.options[language_input.selectedIndex].value;
	editor.setOption("mode", language);
}

function selectTheme() {
	var input = document.getElementById("select_theme");
    var theme = input.options[input.selectedIndex].textContent;
    editor.setOption("theme", theme);
}

function type_selection(){
	var selection_menu = document.getElementById("select_type");
	for (var i = 0; i < selection_menu.options.length; i++){
		show_hide(selection_menu.options[i].value, selection_menu.options[i].selected);
	}
}

function show_hide(id, selected){
	var option_menu = document.getElementById(id);
	if (selected){
		option_menu.style.display = "block";
	}else{
		option_menu.style.display = "none";
	}
}

function add(){
	console.log("add");	
	var type_input = document.getElementById("select_type");
    var type = type_input.options[type_input.selectedIndex].value;
    
    var title = document.getElementById("title").value;
    console.log(type);
    if (type == "code"){
    	console.log("add_code method");
		add_code(title);
	}else if (type == "question"){
		add_question(title);
	}else if (type == "findout"){
		add_findout(title);
	} 
	
}

function add_code(title){	
	var language_input = document.getElementById("select_language");
    var language = language_input.options[language_input.selectedIndex].value;
    console.log(language);
    
    var form_data = {
    	title: title,
    	code: editor.getValue(),
    	language: language
    }  
    
    $.ajax({
    	type: "post",
    	url: "/articles/create_code_snippet",
    	data: JSON.stringify(form_data),
    	contentType: 'application/json;charset=UTF-8',
    	success: function(data){
    		var errorObj = $.parseJSON(data);
			if (!errorObj.iserror){
				window.location = "/";
			}else{
				console.log(errorObj.message);
			}
    	}
    });
}

function add_question(title){
	var question = document.getElementById("question_text").value;

    var form_data = {
    	title: title,
    	question: question
    }  
    
    $.ajax({
    	type: "post",
    	url: "/articles/create_question",
    	data: JSON.stringify(form_data),
    	contentType: 'application/json;charset=UTF-8',
    	success: function(data){
    		var errorObj = $.parseJSON(data);
			if (!errorObj.iserror){
				window.location = "/";
			}else{
				console.log(errorObj.message);
			}
    	}
    });
}

function add_findout(title){
	var findout = document.getElementById("findout_text").value;

    var form_data = {
    	title: title,
    	findout: findout
    }  
    
    $.ajax({
    	type: "post",
    	url: "/articles/create_findout",
    	data: JSON.stringify(form_data),
    	contentType: 'application/json;charset=UTF-8',
    	success: function(data){
    		var errorObj = $.parseJSON(data);
			if (!errorObj.iserror){
				window.location = "/";
			}else{
				console.log(errorObj.message);
			}
    	}
    });
}