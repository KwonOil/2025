function popup(){
    let newWin = window.open('popup.html', '팝업1','left = 0, top = 0, width = 500, height = 300');
    if(newWin == null){
        alert("팝업이 차단되어 있습니다. 팝업 차단을 해제해 주세요.");
    }
    // window.open('popup.html', '팝업2','left = 100, top = 100, width = 500, height = 300');
    // window.open('popup2.html', '팝업3','left = 200, top = 400, width = 500, height = 300');
}