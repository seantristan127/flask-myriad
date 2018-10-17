

$(document).ready(function(){
    $.getJSON("http://127.0.0.1:5000/browse_books",
        function(data){
          $.each(data.products, function(i,product){
            content = '<p>' + product.product_title + '</p>';
            content += '<p>' + product.product_short_description + '</p>';
            content += '<img src="' + product.product_thumbnail_src + '"/>';
            content += '<br/>';
            $(content).appendTo("#product_list");
          });
        });
});
