
var detailUrl = "/detail/?operation_id=";
$("div[id^=detail-]").click(function(){
  var id = $(this).attr('id').substr(7);
  window.location.href = detailUrl + id;
});

/*车源详情卡片的动画效果*/
$("div[id^=detail-]").mouseenter(function(){
  var id = $(this).attr('id').substr(7);
  $("#detail-"+id).animate({right:'10px'});
});

$("div[id^=detail-]").mouseleave(function(){
  var id = $(this).attr('id').substr(7);
  $("#detail-"+id).animate({right:'0px'});
});

$("div[id^=detail-]").hover(function(){
  $(this).css({"cursor": "pointer"});
});

$("#priceSorting").click(function(){
  if($(this).attr("class") == "price-up-sorting"){
    window.location.href = "/search/?priceSortingType=up";
  } else{
    window.location.href = "/search/?priceSortingType=down";
  }
});

$("#updateTimeSorting").click(function(){
  if($(this).attr("class") == "time-up-sorting"){
    window.location.href = "/search/?timeSortingType=up";
  } else{
    window.location.href = "/search/?timeSortingType=down";
  }
});

// 需求面板

var activeColor = "orangered";
var defaultColor = "black";

var conditionSelectedDict = {
  "brand": "",
  "series": "",
  "carModel": "",
  "province": "",
  "city": "",
  "lowestPrice": "",
  "highestPrice": "",
  "shipType": "",
  "color": "",
  "payment": "",
  "carType": "",
  "logistics": "",
};


var searchEngineBaseUrl = "/keyWordSort/"; 

// 将需求字段合并成GET请求格式的url字符串
function encodeURL(){
  var httpGET = searchEngineBaseUrl + "?"
  var i = 0;
  var dictLength = Object.keys(conditionSelectedDict).length;

  for (var key in conditionSelectedDict){

    var value = conditionSelectedDict[key];

    if ((i != 0)&&(i < dictLength) && (value != "")){
      httpGET += "&&";
    }

    if (value != ""){
      httpGET += key + "=" + value;
      i++;
    }    
  }

  return httpGET;
}

function sendGETQuery(){
  window.location.href = encodeURL();
}

$("#brandSelector").change(function(){
  $("#selected-condition-brand").text($("#brandSelector option:selected").text());
  conditionSelectedDict.brand = $("#brandSelector option:selected").text();
  sendGETQuery();
});

$("#seriesSelector").change(function(){
  $("#selected-condition-series").text($("#seriesSelector option:selected").text());
  conditionSelectedDict.series = $("#seriesSelector option:selected").text();
  sendGETQuery();
});

$("#carModelSelector").change(function(){
  $("#selected-condition-car-type").text($("#carModelSelector option:selected").text());
  conditionSelectedDict.carModel = $("#carModelSelector option:selected").text();
  sendGETQuery();
});

$("#region-option-1").click(function(){
  $("#selected-condition-province").text($("#region-option-1 option:selected").text());
  conditionSelectedDict.province = $("#region-option-1 option:selected").text();
  sendGETQuery();
});

$("#region-option-2").change(function(){
  $("#selected-condition-city").text($("#region-option-2 option:selected").text());
  conditionSelectedDict.city = $("#region-option-2 option:selected").text();
  sendGETQuery();
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

              // 更新已选中需求字段
              switch(conditionBarList[j]){
                case "#ship-date":
                  conditionSelectedDict.shipType = $(item).children().text();
                  sendGETQuery();
                  break;
                case "#color":
                  conditionSelectedDict.color = $(item).children().text();
                  sendGETQuery();
                  break;
                case "#payment":
                  conditionSelectedDict.payment = $(item).children().text();
                  sendGETQuery();
                  break;
                case "#car-type":
                  conditionSelectedDict.carModel = $(item).children().text();
                  sendGETQuery();
                  break;
                case "#logistics":
                  conditionSelectedDict.logistics = $(item).children().text();
                  sendGETQuery();
                  break;
                default:
                  break;
              }
            }
          } else {
            $(item).children().css("color", defaultColor);
          }
        });
      }
    });
  }
}

// 保存需求按钮

$("#svae-demand").click(function(){

  $.ajax({
    type: "POST",
    url: "/saveSearchRecord/",
    data: {
      brand: $("#selected-condition-brand").text(),
      series: $("#selected-condition-series").text(),
      carModel: $("#selected-condition-car-type").text(),      
      province: $("#selected-condition-province").text(),
      city: $("#selected-condition-city").text(),
      payment: $("#selected-condition-0").text(),
      color: $("#selected-condition-1").text(),
      shipType: $("#selected-condition-2").text(),
      carType: $("#selected-condition-3").text(),
      logistics: $("#selected-condition-4").text()
    },
    success: function(ret){
        $("#selected-condition-panel li").each(function(i,item){
          $(".selected-condition").text("");
        }); 
    },
    error: function() {alert("需求提交失败，请重试！")}
    });  
});
