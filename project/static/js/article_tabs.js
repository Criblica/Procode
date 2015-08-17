$(document).ready(function() {
	var href = window.location.href;

	var url_parts = href.split("/");
	var article_type = url_parts[url_parts.length-1];
	$("#"+article_type).addClass('active').siblings().removeClass('active');

    /*$('.tabs .tab-links a').on('click', function(e)  {
        var currentAttrValue = $(this).attr('href');
        console.log(currentAttrValue);
        $('.tabs ' + currentAttrValue).show().siblings().hide();
 
        $(this).parent('li').addClass('active').siblings().removeClass('active');
 
        e.preventDefault();
    });*/
});