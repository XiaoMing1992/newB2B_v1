/**
 * Created by panxl on 2016/2/12.
 */
var currentDemandId = 0;

$("a[id^=edit-]").click(function(){
  var demandId = $(this).attr('id').substr(5);

  currentDemandId = demandId;
  // 初始化需求编辑面板的数据
  var demandFiled = ["#brand-",
                    "#series-",
                    "#region-",
                    "#color-",
                    "#payment-",
                    "#type-",
                    "#logistics-"];
  var displayPanelTag = ["brand",
                          "series",
                          "region",
                          "0",
                          "1",
                          "2",
                          "3",
                          "4"];

  for (var i=0; i<demandFiled.length; i++){

    if ($(demandFiled[i] + demandId).text() != ""){
      $("#selected-condition-" + displayPanelTag[i]).text($(demandFiled[i]+demandId).text());
    }
    else {
      $("#selected-condition-brand" + displayPanelTag[i]).text("");
    }
  }

  $("#demandSettingDialog").modal("show");

});

$("a[id^=delete-]").click(function(){
  var demandId = $(this).attr('id').substr(7);

  $.ajax({
    type: "POST",
    url: "/myDemandPost/",
    data: {
      actionType: 0,
      demandId: demandId},
    success: function(ret){
        console.log(ret);
        if (ret=='1'){
          console.log("success");
          $("#demand-"+demandId).remove();
        }
    },
    error: function() {alert("删除失败，请重新操作！")}
  });
});

// 需求面板

var activeColor = "orangered";
var defaultColor = "black";

$("#brandSelector").change(function(){
  $("#selected-condition-brand").text($("#brandSelector option:selected").text());
});

$("#seriesSelector").change(function(){
  $("#selected-condition-series").text($("#seriesSelector option:selected").text());
});

$("#region-option-1").click(function(){
  $("#selected-condition-region").text($(this).text());
});

$("#region-option-2").change(function(){
  $("#selected-condition-region").text($("#region-option-2 option:selected").text());
});

// 通过ul标签绑定关键字链接点击事件

var conditionBarList = ["#ship-date",
                        "#color",
                        "#payment",
                        "#car-type",
                        "#logistics"];

for (var i=0; i<conditionBarList.length; i++){

  // 由于js的变量作用域问题，此处应该使用闭包函数或者with关键词访问变量i
  with ({k: i}){
    $(conditionBarList[k]+" li").click(function(){
      var currentTagId = $(this).attr("id");

      with ({j: k}){
        $(conditionBarList[j]+" li").each(function(i,item){
          var itemId = $(item).attr("id");

          if (itemId == currentTagId){
            $(item).children().css("color", activeColor);
            if ($(item).children().text() == "不限"){
              $("#selected-condition-"+j).hide();
            } else {
              $("#selected-condition-"+j).show();
              $("#selected-condition-"+j).text($(item).children().text());
            }
          } else {
            $(item).children().css("color", defaultColor);
          }
        });
      }
    });
  }
}

$("#save-demand").click(function(){
  // TODO:表单验证

  // 保存时间为当前时间
  var currentDate = new Date();
  var curYear = currentDate.getFullYear();
  var curMonth = currentDate.getMonth();
  var curDay = currentDate.getDate();

  // 过期时间的月份、日期不超过10时，前面为0.比如，01月。
  var exceedDate = $("#exceedDate").val();
  var exceedYear = exceedDate.substring(6, 10);
  var exceedMonth = exceedDate.substring(3, 5);
  var exceedDay = exceedDate.substring(0, 2);

  var demandList = {"demand_id": currentDemandId,
                    "brand": $("#selected-condition-brand").val(),
                    "series": $("#selected-condition-series").val(),
                    "lowest_price": $("#lowest-price").val(),
                    "highest_price": $("#highest-price").val(),
                    "region": $("#selected-condition-region").val(),
                    "save_date":
                      {"year": curYear,
                       "month": curMonth,
                       "day": curDay},
                    "expiry_date":
                        {"year": exceedYear,
                         "month": exceedMonth,
                         "day": exceedDay},
                    "ship-date": $("#selected-condition-0").val(),
                    "color": $("#selected-condition-1").val(),
                    "payment": $("#selected-condition-2").val(),
                    "type": $("#selected-condition-3").val(),
                    "logistics": $("#selected-condition-4").val()};

  $.ajax({
    type: "POST",
    url: "/myDemandPost/",
    data: {
          actionType: 1,
          demand_id: demandList['demand_id'],
          brand: demandList['brand'],
          series: demandList['series'],
          lowest_price: demandList['lowest_price'],
          highest_price: demandList['highest_price'],
          region: demandList['region'],
          save_date: demandList['save_date'],
          expiry_date: demandList['expiry_date'],
          ship_date: demandList['ship-date'],
          color: demandList['color'],
          payment: demandList['payment'],
          type: demandList['type'],
          logistics: demandList['logistics']
        },
    success: function(ret){
        if (ret=='1'){
          $("#demandSettingDialog").modal("hide");
        }
    },
    error: function() {alert("需求保存失败，请重新操作！")}
  });
});