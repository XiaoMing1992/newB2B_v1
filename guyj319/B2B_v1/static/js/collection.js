
$("a[id^=remove-]").click(function(){
  var detailId = $(this).attr('id').substr(7);

  $.ajax({
    type: "POST",
    url: "/collectionPost/",
    data: { detailId: detailId },
    success: function(ret){
      if (ret=='1'){
        $("#blank-"+detailId).remove();
        $("#detail-"+detailId).remove();
      }
    },
    error: function() {alert("请求数据失败，请重新操作！")}
  });
});

$("a[id^=merchant-remove-]").click(function(){
  var merchantId = $(this).attr('id').substr(16);

  $.ajax({
    type: "POST",
    url: "/collectionPost/",
    data: { merchantId: merchantId },
    success: function(ret){
      if (ret=='1'){
        $("#merchant-"+merchantId).remove();
      }
    },
    error: function() {alert("请求数据失败，请重新操作！")}
  });

});