
// 删除消息按钮
$("button[id^=delete-]").click(function(){
    var id = $(this).attr('id').substr(7);

    $.ajax({
        type: "POST",
        url: "/myMessagePost/",
        data: {id: id},
        success: function(ret){
            if (ret=='1'){
              $("#moment-"+id).remove();
              $("#message-"+id).remove();
            }
        },
        error: function() {alert("删除失败，请重新操作！")}
    });
});