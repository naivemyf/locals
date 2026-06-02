$(function(){
    $("#add_save").click(function () {
        Doadd();

    })
})
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function Doadd(){
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url:"/commdity/add/",
        type:"post",
        data:$("#CommdityList").serialize(),
        dataType:"JSON",
        headers:{"X-CSRFToken": csrftoken},
    })
}
