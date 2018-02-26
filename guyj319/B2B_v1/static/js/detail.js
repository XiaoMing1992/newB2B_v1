
// TODO:通过$(this).css()设置样式失败，请检查原因。

var merchantButtonId = "#collectMerchant";
var infoButtonId = "#collectInfo";

$(merchantButtonId).click(function(){
  // 通过样式判断收藏的状态
	if ($(merchantButtonId).css("background-color") != "rgb(170, 170, 170)"){

		var merchantId = $("div[id^=merchant-]").attr('id').substr(9);
		$.ajax({
      type: "POST",
      url: "/detailPost/",
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
	}
});


$(infoButtonId).click( function(){

	if ($(infoButtonId).css("background-color") != "rgb(170, 170, 170)"){
		var infoId = $("div[id^=detail-]").attr('id').substr(7);
		$.ajax({
		type: "POST",
		url: "/detailPost/",
		data: {infoId: infoId},
		success: function(ret){
			switch (ret){
				case "1":
					$(infoButtonId).text("信息已收藏!");
					$(infoButtonId).css({"background-color": "#aaa"});
					break;
				case "0":
					alert("收藏失败，请重新收藏商家！");
					break;
			}
		},
		error: function() {alert("收藏失败，请重新收藏车源！")}
		});
	}
});
