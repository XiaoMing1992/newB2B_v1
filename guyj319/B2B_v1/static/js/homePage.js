
// 撤销发布按钮
$("button[id^=delete-]").click(function(){
  var collectionId = $(this).attr('id').substr(7);

  $.ajax({
    type: "POST",
    url: "/homePagePost/",
    data: {collectionId: collectionId},
    success: function(ret){
      if (ret=='1'){ $("#publish-content-"+collectionId).remove(); }
    },
    error: function() {alert("删除失败，请重新操作！")}
  });
});

// 删除记录按钮
$("button[id^=exceed-delete-]").click(function(){
  var exceedCollectionId = $(this).attr('id').substr(14);
  console.log(exceedCollectionId);

  $.ajax({
    type: "POST",
    url: "/homePagePost/",
    data: {exceedCollectionId: exceedCollectionId},
    success: function(ret){
      if (ret=='1'){ $("#exceed-content-"+exceedCollectionId).remove(); }
    },
    error: function() {alert("删除失败，请重新操作！")}
  });
});