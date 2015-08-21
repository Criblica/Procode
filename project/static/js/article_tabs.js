$(document).ready(function() {
	var href = window.location.href;

	var url_parts = href.split("/");
	var article_type = url_parts[url_parts.length-1];
	$("#"+article_type).addClass('active').siblings().removeClass('active');
});