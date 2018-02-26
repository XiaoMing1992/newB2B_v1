
// 检查手机号码的有效性
function checkPhoneNumber(phoneNumber){
  var reg = /^1[3458]\d{9}$/;

  return reg.test(phoneNumber);
}

// 设置添加联系人按钮的响应事件
var maxContact = 3;
var contactCounter = 1;

$("#addContact").bind("click", function(){
  if (contactCounter < maxContact){
      var newContact = "<input type=\"text\" class=\"form-control\""
              + "id=\"contact" + parseInt(contactCounter) + "\" " +
              "placeholder=\"请输入手机号\">";
      $("#contactContainer").append(newContact);
      contactCounter++;
  }
  else{
      $("#errorTip").text("最多只能添加2个联系人!");
  }
});

var postTime = 0;
var MAX_POST = 2;

// 向服务器发送数据并接收状态码
$("#sendInvitationCode").bind("click", function(){
    if (postTime > MAX_POST){
        alert("1分钟内最多只能发送两次邀请码!");
    }
    else{
        // TODO: 验证表单
        var phoneNumberList = [$("#contact").val(),
                               $("#contact1").val(),
                               $("#contact2").val()];

        var isPhoneNumberValid = true;

        for (var i=0; i<contactCounter; i++){
          if (checkPhoneNumber(phoneNumberList[i]) == false){
            isPhoneNumberValid = false;
            break;
          }
        }
        if (isPhoneNumberValid) {
          $.ajax({
              type: "POST",
              url: "/sendInvitationCode/",
              data: {
                  phoneNumberList: phoneNumberList
              },
              success: function(ret){
                  switch (ret){
                      case "0":
                          alert("邀请码发送失败!");
                          break;
                      case "1":
                          alert("邀请码发送成功!");
                          break;
                      case "2":
                          alert("操作过于频繁，请1小时候再尝试!");
                          break;
                      default: alert("系统内部错误!");
                  }
              },
              error: function() {alert("系统内部错误")}
          });
        }
        else{ $("#errorText").text("请输入有效的手机号") }
    }

    postTime++;
});