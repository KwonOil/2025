function print(value = ""){
    const div = document.createElement("div");
    div.innerHTML = value;
    document.body.appendChild(div);
}

function print2(value = "", sep = "<br>"){
    const div = document.createElement("div");
    document.body.appendChild(div);
    div.innerHTML = (value + sep);
}

function cprint(...args){
    console.log(...args);
}

// 랜덤 함수
function RandomInt(min, max){
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// 쿠키 설정(이름, 값, 유효기간)
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

// 쿠키 가져오기(이름)
function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for(let i=0;i < ca.length;i++) {
        let c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

const apiKey = 'da6dae7bf19dd1d89fe7cad070e71b06';