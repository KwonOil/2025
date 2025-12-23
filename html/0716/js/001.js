// 기본 형식 : $.get("",function(){});
// $.get("http://192.168.0.169/sample1.php",function(data){
//     $("#result").html(data);
// });

$.get("http://192.168.0.169/sample1.php", "do=read&A=1&B=2&C=3", function(info){
    setTimeout(function(){
        $("#result").html(info);
    },2000);
});

$.get("http://192.168.0.169/sample1.php", {do:'create',a:1,b:2,c:3}, function(info){
    $("#result2").html(info);
});

$.get("http://192.168.0.169/sample1.php", "do=update&A=1&B=2&C=3", function(info){
    $("#result3").html(info);
});

$.get("http://192.168.0.169/sample1.php", {do:'delete',1:1,2:2,3:3}, function(info){
    $("#result4").html(info);
});
