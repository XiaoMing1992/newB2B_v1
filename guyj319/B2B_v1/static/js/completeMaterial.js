// 扩展validate.js的手机号码验证功能
$.validator.addMethod("isMobile", function(value, element) {
    var length = value.length;
    var mobile = /^(13[0-9]{9})|(18[0-9]{9})|(14[0-9]{9})|(17[0-9]{9})|(15[0-9]{9})$/;
    return this.optional(element) || (length == 11 && mobile.test(value));
}, "请填写有效的手机号码");

// 隐藏成功后的提示消息
$("#successTip").hide();

var maxContact = 3;
var contactCounter = 1;

$("#addContact").bind("click", function(){
  if (contactCounter < maxContact){
      var newContact = "<div class=\"row\">"
      				    + "<div class=\"form-group\">"
		              + "<div class=\"col-lg-offset-3 col-lg-2\">"
		              + "<input type=\"text\" class=\"form-control\""+ "id=\"contactName"+ contactCounter + "\" name=\"contactName"+contactCounter+"\" placeholder=\"姓名\">"
		              + "</div>"
		              + "<div class=\"col-lg-3\">"
		              + "<input type=\"text\" class=\"form-control\""+ "id=\"phoneNumber" + contactCounter + "\" name=\"phoneNumber"+contactCounter+"\" placeholder=\"联系方式\">"
		              + "</div>"
                  + "</div>"
                  + "</div>";
      $("#contactContainer").after(newContact);
      contactCounter++;   
  }
  else{ $("#contactErrorTip").text("最多只能添加2个联系人!"); }
});


$("#materialForm").validate({
  rules: {
    companyName: { required: true },
    brandIntroduction: { required: true },
    contactName: { required: true },
    phoneNumber: { required: true, isMobile: true },
    licensePhoto: { required: true },
    idCardPhoto: { required: true }
  },
  messages: {
    companyName: { required: "请输入公司名称" },
    brandIntroduction: { required: "请输入主营品牌" },
    contactName: { required: "请输入联系人姓名" },
    phoneNumber: { required: "请完善联系方式"},
    licensePhoto: { required: "请输入营业许可照" },
    idCardPhoto: { required: "请输入身份证照" }
  },submitHandler: function() {
    var companyName = $("#companyName").val();
    var brandIntroduction = $("#brandIntroduction").val();
    var contactNameList = [$("#contactName").val(),
                           $("#contactName1").val(),
                           $("#contactName2").val()];
    var phoneNumberList = [$("#phoneNumber").val(),
                           $("#phoneNumber1").val(),
                           $("#phoneNumber2").val()];
    var merchantType = $('input[name="merchantType"]:checked').val();
    console.log(phoneNumberList);
    console.log(contactNameList);

    $.ajax({
      type: "POST",
      url: "/completeMaterialPost/",
      data: {
        companyName: companyName,
        contactNameList: contactNameList,
        phoneNumberList: phoneNumberList,
        brandIntroduction: brandIntroduction,
        merchantType: merchantType,
        licensePhoto: "licensePhoto",
        idCardPhoto: "idCardPhoto",
        province: $("#province option:selected").val(),
        city: $("#city option:selected").val()
      },
      success: function(ret){
          if (ret=='1'){
            $("#materialForm").hide();
            $("#successTip").show();
          }
          else{ alert("数据提交失败，请稍后重试！");   }
      },
      error: function() { alert("数据提交失败，请稍后重试！"); }
    });
    }
});
