$("p").on("click",function(){
    $("span").css("font-size","50px");
    $("span").css({"font-size":"50px", "color":"red"});
    $("#jq").css({"border":"2px solid orange","background-color":"#73b9ff","color":"#ffff00"});
    
    $(".text").text("텍스트입니다");
    $(".html").html("<h2>HTML입니다</h2>");
});