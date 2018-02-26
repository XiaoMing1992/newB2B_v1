/*
* Author: XingLong Pan
* Date: 2016-04-10
* Description:
*/

$("#logout").click(function (){
  $.ajax({
    type: "post",
    url: "/adminLogout/",
    data: {"action": 1},
    success: function(data){
      if(data === "1"){ window.location = "/adminLogin/"; }
    },
    error: function(){ alert("退出失败，请重试！"); }
  });
});
