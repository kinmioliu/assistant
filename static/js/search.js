$(document).ready(function(){
$('#search-form').submit(function(e){
//console.log("执行了提交"+$(this).serialize());
$.post('/search/', $(this).serialize(), function(data){
//console.log(data);
$('.cmdinfos').html(data);
});
e.preventDefault();
});
});
