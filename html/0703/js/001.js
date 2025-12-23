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
// addBtn이 클릭되면 addList 함수를 실행
document.getElementById("addBtn").addEventListener('click',addList);
// input_text에서 Enter가 눌리면 addList 함수 실행
document.getElementById("input_text").addEventListener('keydown',function(event){
    // console.log(event.key);
    if(event.key == 'Enter') addList();
});
// 이벤트 권한 해제
// document.getElementById("addBtn").removeEventListener('click',addList);