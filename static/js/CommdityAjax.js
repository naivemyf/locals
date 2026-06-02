$(function(){
    $("#add_save").click(function () {
        Doadd();

    })
})
function Doadd(){
        $.ajax({
            url:"/commmdity/add/",
            type:"post",
            data:$("#CommdityList").serialize(),
            dataType:"JSON",
        })
}
 // function btnImageClick() {
 //        $('.motai').click(function () {
 //            let imgSrc = $(this).attr("src");
 //            let imgAlt = $(this).attr("alt");
 //            $("#mtimg").attr("src", imgSrc);
 //            $("#myModalLabel").html(imgAlt);
 //        })
 //    }
