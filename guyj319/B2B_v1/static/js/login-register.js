
// TODO: 这里应该实现函数重载，或者使用工厂模式

// 点击登录对话框中的"没有账号连接，跳转到注册对话框"
$('#toRegister').click(function () {
  $('#loginDialog').modal('hide');
  $('#invitationCodeDialog').modal('show');
});

// 点击注册对话框中的“已有账号链接，跳转到登录对话框”
$('#toLogin').click(function (){
  $('#registerDialog').modal('hide');
  $('#loginDialog').modal('show');
});

// 点击邀请码输入对话框中的“已有账号链接，跳转到登录对话框”
$('#invitationToLogin').click(function (){
  $('#invitationCodeDialog').modal('hide');
  $('#loginDialog').modal('show');
});

// 点击注册成功后的对话框中的“已有账号链接，跳转到登录对话框”
$('#registerToLogin').click(function (){
  $('#registerSuccessDialog').modal('hide');
  $('#loginDialog').modal('show');
});


// 检查手机号码的有效性。如果有效则提交发送验证码请求，否则给出提示。
$("#getVerifyCode").bind("click", function (){

  var reg = /^1[3458]\d{9}$/;
  var mobile = $('#registerPhoneNumber').val();

  if (!(reg.test(mobile))){
    alert('请输入有效的手机号!');
  }
  else{
    //以post方式提交数据
    $.ajax({
    type: "POST",
    url: "/sendPhoneVerifyCode/",
    data: {
        registerPhoneNumber: $("#registerPhoneNumber").val()},
    success: function(ret){
        if (ret == '1'){
            $(this).text("验证码已发送");
            $(this).attr({
              "class": "btn btn-warning btn-block"
            });
        }else{ $(this).text("验证码发送失败!"); }
    },
    error: function() {alert("系统内部错误")}
    });
  }
});

// 点击注册按钮，验证表单后以post方式提交数据。
$("#register").click(function(){
    // TODO: 验证表单
    // 提交数据
    $.ajax({
      type: "POST",
      url: "/verifyRegister/",
      data: {
          phoneNumber: $("#registerPhoneNumber").val(),
          userName: $("#userName").val(),
          password: $("#password").val(),
          verifyCode: $("#verifyCode").val()},
      success: function(ret){
          if (ret=='1'){
              $('#registerDialog').modal('hide');
              $('#registerSuccessDialog').modal('show');
          }
          else{
              $('#invitationCodeTip').html('注册失败!');
          }
      },
      error: function() {alert("注册失败,请重试!")}
    });
});

$("#searchForm").validate({
    rules: {
        brandSelector: { required: true },
        seriesSelector: { required: true }
    },
    errorPlacement: function(error, element) {
        $("#errorTip").text(error.text());
   },
    messages: {
        brandSelector:{ required: "请输入品牌!" },
        seriesSelector: { required: "请输入车系!" }
    }
});

$("#loginForm").validate({
    rules: {
        loginUserName: { required: true },
        loginPassword: { required: true, minlength: 6}
    },
    messages: {
        loginUserName:{ required: "请输入用户名!" },
        loginPassword: { required: "请输入密码!",
                          minlength: "密码长于不小于6位"}
    },
    submitHandler: function(){
      var avoidLogin = 0;
      if ($("#rememberPassword").is(":checked")) avoidLogin = 1;

      $.ajax({
        type: "POST",
        url: "/verifyLogin/",
        data: {
            userName: $("#loginUserName").val(),
            password: $("#loginPassword").val(),
            avoidLogin: avoidLogin},
        success: function(ret){
            if (ret=='1'){
              // 刷新该页面，加载新登录后的页面
              location.reload(true);
            }else {
              $("#loginPasswordErrorTip").text("用户名或密码错误");
            }
        },
        error: function() {$("#loginPasswordErrorTip").text("登录失败，请重试");}
      });
    }
});

$("#invitationForm").validate({
    rules: {
        invitationCode: { 
          required: true,
          maxlength: 6,
          minlength: 6 }
    },
    messages: {
        invitationCode:{ 
          required: "请输入邀请码!", 
          maxlength: "邀请码不能多于6个字符", 
          minlength: "邀请码不能少于6个字符" }
    },
    submitHandler: function() {
      var invitationCode = $('#invitationCode').val();
      $.ajax({
        type: "POST",
        url: "/verifyInvitationCode/",
        data: {invitationCode: invitationCode},
        success: function(ret){
            if (ret=='1'){
                $('#invitationCodeDialog').modal('hide');
                $('#registerDialog').modal('show');
            }
            else{
                $('#invitationCodeTip').text('邀请码失效!');
            }
        },
        error: function() {$('#invitationCodeTip').text('数据提交失败，请稍后重试！');}
      });
    }
});

$("#registerForm").validate({
    rules: {
        registerPhoneNumber: { required: true },
        verifyCode: { required: true, 
                      minlength: 6, 
                      maxlength: 6},
        userName: { required: true },
        password: { required: true,
                    minlength: 6},
        repeatPassword: { required: true,
                          minlength: 6},
        agreement: { required: true }
    },
    messages: {
        registerPhoneNumber: { required: "请输入注册手机号" },
        verifyCode: { required: "请输入手机验证码", 
                      minlength: "验证码长度不少于6个字符", 
                      maxlength: "验证码长度不多于6个字符"},
        userName: { required: "请输入用户名" },
        password: { required: "请设置密码",
                    minlength: "密码长度不少于6个字符"},
        repeatPassword: { required: "请确认密码",
                          minlength: "密码长度不少于6个字符"},
        agreement: { required: "请先同意我们的协议，然后才能注册！" }
    },
    submitHandler: function(form){
      $.ajax({
        type: "POST",
        url: "/verifyRegister/",
        data: {
            phoneNumber: $("#registerPhoneNumber").val(),
            userName: $("#userName").val(),
            password: $("#password").val(),
            verifyCode: $("#verifyCode").val()},
        success: function(ret){
            if (ret=='1'){
                $('#registerDialog').modal('hide');
                $('#registerSuccessDialog').modal('show');
            }
            else{
                $('#invitationCodeTip').html('注册失败!');
            }
        },
        error: function() {alert("注册失败,请重试!")}
      });
    }
});
