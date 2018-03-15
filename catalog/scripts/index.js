$(function() {
(function(context) {
    var pnum = 1
    console.log('Category id is ' + context.cid);
    console.log('URL is ' + "/catalog/index.products/" + context.cid + "/" + pnum + "/");
    $("#products").load("/catalog/index.products/" + context.cid + "/" + pnum + "/");
    $("#next").click(function() {
      if (pnum != context.pnum) {
        $("#products").load("/catalog/index.products/" + context.cid + "/" + (pnum += 1) + "/");
        $("#page-number").text(pnum);
        console.log(pnum);
      }
    });
    //TESTING
    $("#new-next").click(function() {
      if (pnum != context.pnum) {
        $("#products").load("/catalog/index.products/" + context.cid + "/" + (pnum += 1) + "/");
        $("#page-number").text(pnum);
        console.log(pnum);
      }
    });
    //TESTING
    $("#previous").click(function() {
      if (pnum != 1) {
        $("#products").load("/catalog/index.products/" + context.cid + "/" + (pnum -= 1) + "/");
        $("#page-number").text(pnum);
        console.log(pnum);
      }
    });
    //TESTING
    $("#new-previous").click(function() {
      if (pnum != 1) {
        $("#products").load("/catalog/index.products/" + context.cid + "/" + (pnum -= 1) + "/");
        $("#page-number").text(pnum);
        console.log(pnum);
      }
    });
    //TESTING
    //TESTING
    $("#change-page").click(function() {
        $("#products").load("/catalog/index.products/" + context.cid + "/" + (pnum = 2) + "/");
        $("#page-number").text(pnum);
        $("#page-changer").addClass('active');
        console.log(pnum);
    });
    //TESTING
})(DMP_CONTEXT.get());
})
