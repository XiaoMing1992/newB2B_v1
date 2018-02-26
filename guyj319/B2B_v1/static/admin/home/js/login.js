/*
* Author: XingLong Pan
* Date: 2016-04-10
* Description:
*/

$("#login").click(function() {

  $.ajax({
    type: "post",
    url: "/adminLoginPost/",
    data: {
      "user_name": $("#user_name").val(),
      "password": $("#password").val()
    },
    success: function(data){
      if(data === "1"){
        // TODO: success
        window.location.href = "/adminHome/";
      }
      else{ // TODO:　用户名或密码错误
      }
    },
    error: function(){ alert("登陆失败，请重试！"); }
  });
});
