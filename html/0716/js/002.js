// 기본 형식 : $.ajax("주소"[,매개변수][,콜백함수]);
//$.ajax("");

// $.ajax("sample2.html").done(function(info) {
//     alert("요청 성공");
//     $("#result").html(info);
// }).fail(function() {
//     alert("요청 실패");
// }).always(function() {
//     //alert("요청 완료");
// });

// // get방식
// $.ajax({
//     url : "sample2.html",
//     type : "GET",
//     datatype : "html",
//     data : { do:'read', name : '고', age : 20},
//     success : function(info){
//         $("#result").html(info);
//     },
//     error: function(){
//         cprint("요청실패");
//     },
//     complete : function(){
//         cprint("요청완료");
//     }
// });

// // post방식, php
// $.ajax({
//     url : "http://192.168.0.169/sample2.php",
//     type : "GET",
//     datatype : "html",
//     data : { do:'update', name : '홍', age : 20},
//     success : function(info){
//         $("#result2").html(info);
//     },
//     error: function(){
//         cprint("요청실패");
//     },
//     complete : function(){
//         cprint("요청완료");
//     }
// });

// // post방식, 파이썬
// $.ajax({
//     url : "http://192.168.0.169:5000",
//     type : "POST",
//     datatype : "html",
//     data : { do:'delete', name : '김', age : 20},
//     success : function(info){
//         $("#result3").html(info);
//     },
//     error: function(){
//         cprint("요청실패");
//     },
//     complete : function(){
//         cprint("요청완료");
//     }
// });

// // 단순 load
// $("#result4").load("sample2.html");

$.ajax({
    url:"sample.html",
    type : "GET",
    // dataType: "text",
    dataType: "json",
    success: function(info){
        cprint(info);
        // info = JSON.parse(info);
        let html = `
        <h2>이름 : ${info.name}</h2>
        <h2>나이 : ${info.age}</h2>`;
        $("#result").html(html);
    },
    error:function(){
        cprint("요청실패");
    },
    complete:function(){
        cprint("요청성공");
    }
});