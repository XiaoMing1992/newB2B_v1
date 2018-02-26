

var merchantButtonId = "#collectMerchant";
$(merchantButtonId).click(function(){
  var merchantId = $("div[id^=merchant-]").attr('id').substr(9);

  $.ajax({
    type: "POST",
    url: "/merchantPost/",
    data: {merchantId: merchantId},
    success: function(ret){
        switch (ret){
          case "1":
            $(merchantButtonId).text("商家已收藏!");
            $(merchantButtonId).css({"background-color": "#aaa"});
            break;
          case "0":
            alert("收藏失败，请重新收藏商家！");
            break;
        }
      },
      error: function() {alert("收藏失败，请重新收藏商家！")}
  });
});

// 鼠标点击响应
var detailUrl = "/detail/?operation_id=";
$("div[id^=detail-]").click(function(){
  var id = $(this).attr('id').substr(7);
  window.location.href = detailUrl + id;
});

// 车源详情卡片动画效果
$("div[id^=detail-]").mouseenter(function(){
  var id = $(this).attr('id').substr(7);
  $("#detail-"+id).animate({right:'10px'});
});

$("div[id^=detail-]").mouseleave(function(){
  var id = $(this).attr('id').substr(7);
  $("#detail-"+id).animate({right:'0px'});
});

$("div[id^=detail-]").hover(function(){
  $(this).css({"cursor": "pointer"});
});
