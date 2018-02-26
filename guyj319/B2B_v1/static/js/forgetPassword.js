
// 扩展validate.js的手机号码验证功能
$.validator.addMethod("isMobile", function(value, element) {
    var length = value.length;
    var mobile = /^(13[0-9]{9})|(18[0-9]{9})|(14[0-9]{9})|(17[0-9]{9})|(15[0-9]{9})$/;
    return this.optional(element) || (length == 11 && mobile.test(value));
}, "请填写有效的手机号码");


// 实现页面更换
var currentSection = 1;

function updateView (){
  for (var i=1; i<=4; i++){
    if (i==currentSection) {
      $("#form-"+i).show();
    }
    else {
      $("#form-"+i).hide();
    }

    if (i<=currentSection){
      $("#section-"+i).addClass("for-cur");
      $("#icon-"+i).addClass("for-cur");
    }
    else {
      $("#section-"+i).removeClass("for-cur");
      $("#icon-"+i).removeClass("for-cur");
    }
  }
}

// 初始化页面
updateView();

// 表单验证
$("#form-1").validate({
    rules: {
        phoneNumber: {
          required: true,
          isMobile: true
        }
    },
    messages: {
        newPassword:{
          required: "请输入新密码",
          minlength: "密码不得少于6个字符"
        }
    },submitHandler: function(){
      var phoneNumber = $("#phoneNumber").val();

      $.ajax({
        type: "POST",
        url: "/forgetPasswordPost/",
        data: {phoneNumber: phoneNumber},
        success: function(ret){
          if (ret == "0"){ alert("该手机号不存在，请先注册！"); }
          else {
            currentSection = 2;
            updateView();
          }
        },
        error: function() { alert("数据提交失败!"); }
      });
  }
});

$("#form-2").validate({
    rules: { verifyCode: { required: true } },
    messages: { verifyCode:{ required: "验证码不能为空" } },
    submitHandler: function() {
      var verifyCode = $("#phoneVerifyCode").val();

      $.ajax({
        type: "POST",
        url: "/forgetPasswordPost/",
        data: {verifyCode: verifyCode},
        success: function(ret){
          if (ret == "1"){
            currentSection = 3;
            updateView();
          }else { $("#verifyCodeError").text("验证码错误，请重试！"); }
        },
        error: function() { alert("数据提交失败!"); }
      });
    }
});

$("#form-3").validate({
    rules: {
        newPassword: {
          required: true,
          minlength: 6
        },
        repeatePassword: {
          required: true,
          minlength: 6,
          equalTo: "#newPassword"
        }
    },
    messages: {
        newPassword:{
          required: "请输入新密码",
          minlength: "密码不得少于6个字符"
        },
        repeatePassword: {
          required: "两次输入不一致",
          minlength: "密码不得少于6个字符", equalTo: "密码输入不一致"
        }
    },submitHandler: function() {
      var newPassword = $("#newPassword").val();

      $.ajax({
        type: "POST",
        url: "/forgetPasswordPost/",
        data: {newPassword: newPassword},
        success: function(ret){
          if (ret == "1"){
            currentSection = 4;
            updateView();
          }
        },
        error: function() { alert("数据提交失败!"); }
      });
    }
});