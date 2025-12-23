// onload : 모든 리소스가 로딩된 후 실행
window.onload = function(){
    print("window.onload()");
};

// jQuery : DOM 구조만 로딩되면 실행
// jQuery 기본형
$(document).ready(function(){
    print("document.ready()");
});

// jQuery 축약형 : $()
$(function(){
    print("document.ready()2");
});