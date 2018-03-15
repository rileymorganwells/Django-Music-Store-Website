$(function() {
(function(context) {
    var pnum = 1
    console.log('Category id is ' + context.cid);
    console.log('URL is ' + "/catalog/index.products/" + context.cid + "/" + pnum + "/");
    $("#products").load("/catalog/index.products/" + context.cid + "/" + pnum + "/");
    $("#page-changer-"+pnum).addClass('active');
    $("#next").click(function() {
      if (pnum != context.pnum) {
        $("#products").load("/catalog/index.products/" + context.cid + "/" + (pnum += 1) + "/");
        $(".active").removeClass('active');
        $("#page-changer-"+pnum).addClass('active');
        $("#page-number").text(pnum);
        console.log(pnum);
      }
    });
    //TESTING
    $("#new-next").click(function() {
      console.log(pnum);
      if (pnum != context.pnum) {
        $("#products").load("/catalog/index.products/" + context.cid + "/" + (pnum += 1) + "/");
        $(".active").removeClass('active');
        $("#page-changer-"+pnum).addClass('active');
        $("#page-number").text(pnum);
        console.log(pnum);
      }
    });
    //TESTING
    $("#previous").click(function() {
      if (pnum != 1) {
        $("#products").load("/catalog/index.products/" + context.cid + "/" + (pnum -= 1) + "/");
        $(".active").removeClass('active');
        $("#page-changer-"+pnum).addClass('active');
        $("#page-number").text(pnum);
        console.log(pnum);
      }
    });
    //TESTING
    $("#new-previous").click(function() {
      if (pnum != 1) {
        $("#products").load("/catalog/index.products/" + context.cid + "/" + (pnum -= 1) + "/");
        $(".active").removeClass('active');
        $("#page-changer-"+pnum).addClass('active');
        $("#page-number").text(pnum);
        console.log(pnum);
      }
    });
    //TESTING
    //TESTING
    $(".change-page").click(function() {
      var newpage = $(this).text();
      pnum = parseInt(newpage);
        console.log(newpage);
        $("#products").load("/catalog/index.products/" + context.cid + "/" + newpage + "/");
        $("#page-number").text(newpage);
        $(".active").removeClass('active');
        $("#page-changer-"+newpage).addClass('active');
        console.log(pnum);
    });
    //TESTING
})(DMP_CONTEXT.get());
})
