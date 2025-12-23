$.ajax({
    url:"http://192.168.0.169:5500/0716/pre/011_1.html",
    type : "GET",
    dataType: "html",
    success: function(info){
        $("#result").html(info);
    },
    error:function(){
        cprint("요청실패");
    },
    complete:function(){
        cprint("요청완료");
    }
});