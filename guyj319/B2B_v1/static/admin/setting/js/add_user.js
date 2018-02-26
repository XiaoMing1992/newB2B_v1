/*
* Author: XingLong Pan
* Date: 2016-04-12
* Description:
*/

$("#add_new_admin").click(function() {

  $.ajax({
    type: "post",
    url: "/adminAddAdministratorPost/",
    data: {
      "name": $("#name").val(),
      "account": $("#account").val(),
      "password": $("#password").val()
    },
    success: function(data){
      if(data === "1"){
        // TODO: success
        alert("账号添加成功！");
      }
    },
    error: function(){ alert("账号添加失败，请重试！"); }
  });
});
