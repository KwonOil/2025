// form으로 입력받아 엔터 처리하기
function addList(event){
    // 기본 성질(여기선 페이지가 리프레쉬 되는 현상)
    // event.preventDefault();

    let input_text = document.getElementById("input_text").value;
    if(!input_text.trim()) return;
    document.getElementById("numberList").innerHTML += `<li>${input_text}</li>`;
    document.getElementById("input_text").value = "";
    document.getElementById("input_text").focus();
}

function addList(){
    let input_text = document.getElementById("input_text").value;
    if(!input_text.trim()) return;
    document.getElementById("numberList").innerHTML += `<li>${input_text}</li>`;
    document.getElementById("input_text").value = "";
    document.getElementById("input_text").focus();
}

// 이벤트 권한 부여
document.getElementById("addBtn").addEventListener('click',addList);
// 이벤트 권한 해제
// document.getElementById("addBtn").removeEventListener('click',addList);