function showImg(){
    if(document.querySelector("#date").innerHTML){
        document.querySelector("#date").innerHTML = null;
        document.querySelector("button").textContent = "이미지 보여줘!";
    }
    else{
        document.querySelector("#date").innerHTML = "<img width = '50%' src = 'https://i.namu.wiki/i/WtQeUA_hzEAooY850rWvlamC_u0wxJKbnBbp6kamlyy5Xer84isLH5rP9ayO8yjvK3zxjEmhvYtZ-Bb_E3zxQS89wIbdjec8pAQR5Jpa3QFQhEReEfaOgpnLC3GRxSOM4pNdNsPVpcuHTPYavIJFwg.webp'>";
        document.querySelector("button").textContent = "이미지 숨기기!";
    }
}

// syntax sp2 함수
function viewBox(fname){
    document.getElementById('js_intro_intro_02').src = fname;
}

// syntax sp3 함수
function changeSize(){
    document.getElementById('js_intro_intro_03').style.fontSize = '30px';
}

function changeColor(){
    document.getElementById('js_intro_intro_03').style.color ='#ff0000';
}
