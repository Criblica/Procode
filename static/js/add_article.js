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
		linenumbers: true,
		indentWithTabs: true
		//theme: "ambience"
    };

    var editor = CodeMirror.fromTextArea(document.getElementById("editor"), config);
	editor.setSize(500, 100);
	
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

