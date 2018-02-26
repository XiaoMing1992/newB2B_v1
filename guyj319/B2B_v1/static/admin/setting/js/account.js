/*
* Author: XingLong Pan
* Date: 2016-04-11
* Description:
*/

// TODO:　表单验证

$("#submit_change").click(function(){

  $.ajax({
    type: "post",
    url: "/adminAccountSettingPost/",
    data: {
      "name": $("#name").val(),
      "old_password": $("#old_password").val(),
      "new_password": $("#new_password").val()
    },
    success: function(data){
      if(data === "1"){
        // TODO: success
        alert("修改成功！");
      }
      else{
        // TODO:　旧密码错误
        alert("当前密码输入错误！");
      }
    },
    error: function(){ alert("登陆失败，请重试！"); }
  });

});
