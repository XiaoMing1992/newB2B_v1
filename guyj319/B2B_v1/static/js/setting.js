
var isOldPasswordCorrect = false;

$("#oldPassword").blur(function(){
  var oldPassword = $(this).val();

  $.ajax({
    type: "POST",
    url: "/settingPost/",
    data: { oldPassword: oldPassword },
    success: function(ret){
      if (ret != "1"){
        $(".old-password-error").text("当前用户密码错误，请重新输入!");
      }else{
        isOldPasswordCorrect = true;
        $(".old-password-error").text("");
      }
    },
    error: function() { alert("数据提交失败!"); }
  });
});

$("#submitNewPassword").click(function() {
  var successTip = "<div class=\"col-lg-offset-4 col-lg-3\"> " +
                   "<h3 class=\"text-success\">密码修改成功!</h3>" +
                   "</div>";
  var newPassword = $("#newPassword").val();

  if (isOldPasswordCorrect){
    $.ajax({
        type: "POST",
        url: "/settingPost/",
        data: { newPassword: newPassword },
        success: function(ret){
          if (ret == "1"){
            $("#passwordSettingForm").remove();
            $("#passwordSettingPanel").append(successTip);
          }
        },
        error: function() { alert("数据提交失败!"); }
    });
  }
});


// 修改绑定手机号
var isOldPhoneCorrect = false;
var isAuthorized = false;
var isNewPhoneNumberExist = false;
var isVerifyCodeValid = false;

$("#oldPhoneNumber").blur(function(){
  var oldPhoneNumber = $(this).val();

  $.ajax({
    type: "POST",
    url: "/settingPost/",
    data: { oldPhoneNumber: oldPhoneNumber },
    success: function(ret){
      if (ret != "1"){
        $(".old-mobile-error").text("当前输入的手机号错误，请重新输入!");
      }else{
        isOldPhoneCorrect = true;
        $(".old-mobile-error").text("");
      }
    },
    error: function() { alert("数据提交失败!"); }
  });
});

$("#currentPassword").blur(function(){
  var currentPassword = $(this).val();

  $.ajax({
    type: "POST",
    url: "/settingPost/",
    data: { currentPassword: currentPassword },
    success: function(ret){
      if (ret != "1"){
        $(".current-password-error").text("当前输入的密码错误，请重新输入!");
      }else{
        isAuthorized = true;
        $(".current-password-error").text("");
      }
    },
    error: function() { alert("数据提交失败!"); }
  });
});

$("#newPhoneNumber").blur(function(){

  var pattern=/(^(([0\+]\d{2,3}-)?(0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$)/;
  var newPhoneNumber = $(this).val();

  if (pattern.test(newPhoneNumber)){
    $("#newPhoneNumberError").text("当前输入的手机号格式错误，请重新输入!");
  }else{
    isNewPhoneNumberExist = true;
    $.ajax({
        type: "POST",
        url: "/settingPost/",
        data: {newPhoneNumberExist: newPhoneNumber},
        success: function(ret){
          switch (ret){
            case '0':
              break;
            case '1':
              $("#newPhoneNumber").val();
              break;
            case '2':
              $("#newPhoneNumberError").text("该手机号已经被注册，请使用其他号码!");
              break;
          }
        },
        error: function() { alert("数据提交失败!"); }
    });
    $("#newPhoneNumberError").text("");
  }
});

// 检查手机号码的有效性。如果有效则提交发送验证码请求，否则给出提示。
// 发送验证码倒计时

var WAITE_TIME = 60;
var counter = WAITE_TIME;
var getVerifyCode = "#getVerifyCode";

function timeOut(){
  counter--;
  $(getVerifyCode).text(counter+"秒后重新发送");
  $(getVerifyCode).attr("disabled", true);
  if (counter) { setTimeout("timeOut()", 1000); }
  else {
    $(getVerifyCode).text("发送手机验证码");
    $(getVerifyCode).attr("disabled", false );
  }
}

$(getVerifyCode).click(function() {
  var newPhoneNumber = $("#newPhoneNumber").val();

  if (isNewPhoneNumberExist){
    $.ajax({
        type: "POST",
        url: "/sendVerifyCode/",
        data: { phoneNumber: newPhoneNumber },
        success: function(ret){
          switch (ret){
            case '0':
              $("#verifyCodeError").text("发送失败，请重试!");
              break;
            case '1':
              timeOut();
              break;
            case '2':
              $("#verifyCodeError").text("操作过于频繁，请1小时候重试!");
              break;
          }
        },
        error: function() { alert("数据提交失败!"); }
    });
  }
});

$("#verifyCode").blur(function() {
  var newPhoneNumber = $("#newPhoneNumber").val();
  var verifyCode = $(this).val();

  $.ajax({
        type: "POST",
        url: "/verifyCodePost/",
        data: {
          phoneNumber: newPhoneNumber,
          verifyCode: verifyCode },
        success: function(ret){
          if (ret == "1"){ isVerifyCodeValid = true; }
          else { $("#verifyCodeError").text("验证码错误，请重新输入!"); }
        },
        error: function() { alert("数据提交失败!"); }
    });
});

$("#submitNewPhoneNumber").click(function() {
  var successTip = "<div class=\"col-lg-offset-4 col-lg-3\"> " +
                   "<h3 class=\"text-success\">手机号修改成功!</h3>" +
                   "</div>";
  var newPhoneNumber = $("#newPhoneNumber").val();

  if (isOldPhoneCorrect
      && isAuthorized
      && isNewPhoneNumberExist
      && isVerifyCodeValid){
    $.ajax({
        type: "POST",
        url: "/settingPost/",
        data: { newPhoneNumber: newPhoneNumber },
        success: function(ret){
          if (ret == "1"){
            $("#phoneNumberSettingForm").remove();
            $("#phoneNumberSettingPanel").append(successTip);
          }
        },
        error: function() { alert("数据提交失败!"); }
    });
  }
});

