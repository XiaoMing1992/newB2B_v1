/*
* Author: XingLong Pan
* Date: 2016-04-12
* Description:
*/

// 删除账号信息
$("button[id^=delete-]").click(function(){
    var id = $(this).attr('id').substr(7);

    $.ajax({
        type: "POST",
        url: "/adminDeleteAdministratorPost/",
        data: {id: id},
        success: function(ret){
            if (ret=='1'){ $("#tr-"+id).remove() }
            else{ alert("删除失败，请重新操作！") }
        },
        error: function() { alert("删除失败，请重新操作！") }
    });
});
