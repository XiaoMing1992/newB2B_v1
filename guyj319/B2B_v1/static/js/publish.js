

var currentSection = 1;

$("input[name=shipType]:radio").click(function() {
  if($(this).attr("id")=="shipType-2") { $("#shipDate").attr("disabled", false); } 
  else { $("#shipDate").attr("disabled", true); }
});

$("input[name=region]:radio").click(function() {
  switch ($(this).val()){
    case '0':
      $("#province1").attr("disabled", true);
      $("#province2").attr("disabled", true);
      $("#city").attr("disabled", true);
      break;
    case '1':
      $("#province1").attr("disabled", false);
      $("#province2").attr("disabled", true);
      $("#city").attr("disabled", true);
      break;
    case '2':
      $("#province1").attr("disabled", true);
      $("#province2").attr("disabled", false);
      $("#city").attr("disabled", false);
      break;
  }
});

$("a[id^=contact-edit-]").click(function(){
  var id = $(this).attr('id').substr(13);
  $("#contact-icon-"+id).val("done");
  console.log($(this).val());
  console.log(id);
  $("#contactName-"+id).attr("disabled", false);
  $("#phoneNumber-"+id).attr("disabled", false);
});

$("a[id^=contact-delete-]").click(function(){
  var id = $(this).attr('id').substr(15);
  $("#contact-panel-"+id).hide();
});

/**/
$("#add-contact").click(function(){
  var len = $("#contact").children().length;
  var newContactBox = "<div class=\"col-lg-2\" id=\"contact-panel-\">" +
                      "<table class=\"contact-box\">" +
                      "<tr>" +
                      "<td><input type=\"text\" id=\"contactName-1\"" +
                      "value=\"\" placeholder=\"联系人\"/></td>" +
                      "<td>" +
                      "<a href=\"#\" id=\"contact-edit-1\" >" +
                      "<i class=\"material-icons\" id=\"contact-icon-1\">edit</i>"+
                      "</a>" +
                      "</td>" +
                      "</tr>" +
                      "<tr>" +
                      "<td><input type=\"text\" id=\"phoneNumber-1\"" +
                      "value=\"\" placeholder=\"手机号\"/></td>" +
                      "<td><a href=\"#\" id=\"contact-delete-1\"><i class=\"material-icons\">delete</i></a></td>" +
                      "</tr>" +
                      "</table>" +
                      "</div>";

  if (len >= 5){ alert("最多只能添加3个联系人！"); }
  else{ $("#contact-panel-1").show(); }
});


// 由于暂时没有找到jQuery validate插件验证嵌套表单（或者多个平行表单）的方法，
/*表单验证规则说明：
  1、车辆类型至少选择一个选项
  2、必须选择品牌
  3、必须选择车系
  4、必须选择车款
  5、车辆颜色至少选择一个选项
  6、如果选择了期货，必须选择日期
  7、如果选择了全省，必须选择省份
  8、如果选择了全市，必须选择省份、城市
  9、必须填写行价
  10、必须填写已优惠价格（必须小于行价）
  11、必须填写过期时间
*/

function isInputValid(){

  if ( $("[name=specification]:checked").length === 0 ){
    $("#specification-tip").text("请至少选择一个车辆类型");
    return false;
  }

  if ( $("#brand option:selected").val() === "0" ){
    $("#car-type-tip").text("请选择品牌");
    return false;
  }

  if ( $("#series option:selected").val() === "0" ){
    $("#car-type-tip").text("请选择车系");
    return false;
  }

  if ( $("#style option:selected").val() === "0" ){
    $("#car-type-tip").text("请选择车款");
    return false;
  }

  if ($("[name=color]:checked").length === 0){
    $("#color-tip").text("请至少选择一种颜色");
    return false;
  }

  if ( $("#carPrice").val() === "" ){
    $("#price-tip").text("请填写行价");
    return false;
  }

  if ( $("#discountRate").val() === "" ){
    $("#price-tip").text("请填写优惠价格");
    return false;
  }

  if ( parseInt($("#discountRate").val()) > parseInt($("#carPrice").val()) ){
    $("#price-tip").text("填写有误，优惠价格不得高于行价！");
    return false;
  }

  if ( $("#exceedDate").val() === "" ){
    $("#exceed-date-tip").text("请填写过期时间");
    return false;
  }

  return true;
}

// “车源”对象的数据字典
var carDetail = {"specificationList": ["", "", "", ""],
                 "colorList": ["", "", "", "", ""],
                 "brand": "",
                 "series": "",
                 "style": "",
                 "price": 
                   {"carPrice": "", 
                   "discountRate": ""},
                 "region": {"type": "", "province": "", "city": ""},
                 "logistics": "",
                 "shipType": {"type": "", "year": "", "month": "", "day": ""},
                 "payment": "",
                 "comment": "",
                 "exceedDate": {"year": "", "month": "", "day": ""}};

function getCarDetail(){
  $("input[name='specification']").each( function (i) {

    if ($(this).is(":checked")){
      carDetail["specificationList"][i] = $(this).val();
    }
  });

  carDetail["brand"] = $("#brand option:selected").text();
  carDetail["series"] = $("#series option:selected").text();
  carDetail["style"] = $("#style option:selected").text();

  // 颜色
  $("input[name='color']").each( function (i) {

    if ($(this).is(":checked")){
      carDetail["colorList"][i] = $(this).val();
    }
  });

  // 提货时间
  if ($("input[name='shipType']:checked").val() == "现货"){
    carDetail["shipType"]["type"] = "现货";

    // 现货的提货时间为发布车源当天的时间
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    var currentMonth = currentDate.getMonth();
    var currentDay = currentDate.getDate();

    carDetail["shipType"]["year"] = currentYear;
    carDetail["shipType"]["month"] = currentMonth;
    carDetail["shipType"]["day"] = currentDay;      
  }
  else{
    carDetail["shipType"]["type"] = "期货";

    var shipDate = $("#shipDate").val();
    carDetail["shipType"]["year"] = shipDate.substring(6, 10);
    carDetail["shipType"]["month"] = shipDate.substring(3, 5);
    carDetail["shipType"]["day"] = shipDate.substring(0, 2);
  }

  // 支付方式
  carDetail["payment"] = $("input[name='payment']:checked").val();

  // 地区
  if ($("input[name='region']:checked").val() == "0"){
  carDetail["region"]["type"] = "全国";
  } else if($("input[name='region']:checked").val() == "1"){
  carDetail["region"]["type"] = "全省";
  carDetail["region"]["province"] = $("#province1 option:selected").text();
  } else {
  carDetail["region"]["type"] = "全市";
  carDetail["region"]["province"] = $("#province2 option:selected").text();
  carDetail["region"]["city"] = $("#city option:selected").text();
  }

  // 物流方式
  carDetail["logistics"] = $("input[name='logistics']:checked").val();
  console.log($("input[name='logistics']:checked").val());

  // 报价
  carDetail["price"]["carPrice"] = $("#carPrice").val();
  carDetail["price"]["discountRate"] = $("#discountRate").val();

  // 过期时间
  var exceedDate = $("#exceedDate").val();
  carDetail["exceedDate"]["year"] = exceedDate.substring(6, 10);
  carDetail["exceedDate"]["month"] = exceedDate.substring(3, 5);
  carDetail["exceedDate"]["day"] = exceedDate.substring(0, 2);

  // 联系人
  $("#contact1").text();
  // $("#contact2").text($("#contactName-2").val() + " " + $("#phoneNumber-2").val());
  // $("#contact3").text($("#contactName-3").val() + " " + $("#phoneNumber-3").val());

  // 备注说明
  carDetail["comment"] = $("#comment").val();
}

function bindDataToView(){
  $(".car-specification").text(carDetail["specificationList"].join(" "));
  $(".car-type").text(carDetail["brand"] + " " + 
                      carDetail["series"] + " " + 
                      carDetail["style"]);
  $(".color-option").text(carDetail["colorList"].join(" "));
  $(".ship-type").text(carDetail["shipType"]["type"]);
  $(".payment").text(carDetail["payment"]);

  if (carDetail["region"]["type"] === "全国"){
    $(".region").text(carDetail["region"]["type"]);
  }
  else{
    $(".region").text(carDetail["region"]["province"] + " " +
                      carDetail["region"]["city"]);
  }
  $(".logistics").text(carDetail["logistics"]);
  $(".price").text(carDetail["price"]["carPrice"] + " 万|下 " +
                   carDetail["price"]["discountRate"] + "万");
  $(".ship-date").text(carDetail["shipType"]["day"] + "/" +
                       carDetail["shipType"]["month"] + "/" +
                       carDetail["shipType"]["year"]);
  $(".comment").text(carDetail["comment"]);
  $(".exceed-date").text(carDetail["exceedDate"]["day"] + "/" +
                         carDetail["exceedDate"]["month"] + "/" +
                         carDetail["exceedDate"]["year"]);
}

$("#submitCarForm").click(function (){

  if (isInputValid()){
    // 将数据存储到carDetail对象
    getCarDetail();

    // 将数据绑定到预览页面
    bindDataToView();
    
    // 更新页面
    currentSection = 2;
    updateView();
  }
});

// 实现页面更换

function updateView (){
  for (var i=1; i<=4; i++){
    if (i==currentSection) {
      $("#section-"+i).show();
    }
    else {
      $("#section-"+i).hide();
    }
  }
}

// 初始化页面
updateView();

$("#return-to-edit").click(function(){
  currentSection = 1;
  updateView();
});

$("#publish-car").click(function(){

  $.ajax({
    type: "POST",
    url: "/publishPost/",
    data: {
      "specificationList": carDetail["specificationList"],
      "colorList": carDetail["colorList"],
      brand: carDetail["brand"],
      series: carDetail["series"],
      style: carDetail["style"],
      price: carDetail["price"],
      region: carDetail["region"],
      logistics: carDetail["logistics"],
      shipType: carDetail["shipType"],
      payment: carDetail["payment"],
      comment: carDetail["comment"],
      exceedDate: carDetail["exceedDate"]
    },
    success: function(ret){
        if (ret=='1'){
          currentSection = 3;
          updateView();
        }
        else{
            alert("车源发布失败,请重试2!");
        }
    },
    error: function() { alert("车源发布失败,请重试!") }
  });
});
