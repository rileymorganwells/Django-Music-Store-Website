(function(context) {
    // utc_epoch comes from index.py
    console.log('Current epoch in UTC is ' + context.utc_epoch);
    return function() {
      //need 3 functions - page_load
      //  -left button
      //  -right button $("#prevpage"). click(function() {
      //            $("#products").load("/catalog/index.products/" + context.cid + pagenum)})

   }

})(DMP_CONTEXT.get());
