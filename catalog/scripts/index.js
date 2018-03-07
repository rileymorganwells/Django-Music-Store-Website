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
    $("#previous").click(function() {
      if (pnum != 1) {
        $("#products").load("/catalog/index.products/" + context.cid + "/" + (pnum -= 1) + "/");
        $("#page-number").text(pnum);
        console.log(pnum);
      }
    });
})(DMP_CONTEXT.get());
})
