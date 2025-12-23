// 웹 브라우저의 위치 관련 정보 확인 메서드들
function printInfo(){
    document.body.innerHTML = '';
    print(`웹 브라우저의 너비: ${window.innerWidth}`);
    print(`웹 브라우저의 높이: ${window.innerHeight}`);
    print(`웹 브라우저 창의 너비: ${window.outerWidth}`);
    print(`웹 브라우저 창의 높이: ${window.outerHeight}`);
    print(`웹 브라우저 창 위쪽 면과 모니터 사이의 간격: ${window.screenTop} / ${window.screenY}`);
    print(`웹 브라우저 창 왼쪽 면과 모니터 사이의 간격: ${window.screenLeft} / ${window.screenX}`);
    print(`웹 브라우저 창의 스크롤 가로 위치: ${window.scrollX}`);
    print(`웹 브라우저 창의 스크롤 세로 위치: ${window.scrollY}`);
}
window.innerWidth = 1000;