$(function() {
  $('.images').mouseenter(function(){
    var src = $(this).attr('src');
    $('#main-image').attr('src',src);
  })
})
