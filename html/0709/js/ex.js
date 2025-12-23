// 변수 정의

// let todoList = [];
// 서버에 저장되어 있던 JSON 불러와서 파싱해서 todoList에 저장
let todoList = JSON.parse(localStorage.getItem('todoList')) || [];

// todoList.push("공부");
// todoList.push("청소");
// todoList.push("점심");
// todoList.push("면접");

// 렌더 함수
function render(list){
    let div = document.querySelector("#content");
    let lastResult = "";
    lastResult += "<ul>";
    list.forEach((element,i) => {
        lastResult += `<li><span class="item-text">▶ ${element}</span><button class ="removeBtn" onclick = "remove(${i})">삭제</button></li>`;
    });
    lastResult += "</ul>";
    div.innerHTML = lastResult;
}

// 초기화 함수
function initTodo() {
    localStorage.removeItem('todoList');
    todoList = [];
    renderTodoList(todoList);
}

// 추가 함수
function add(){
    let inputText = document.querySelector("#inputText");
    let newItem = inputText.value;
    inputText.value = "";
    if(newItem){
        todoList.push(newItem);
    }
    render(todoList);
    saveToLocalStorage();
}

// 엔터 칠 때도 add 실행
document.querySelector("#inputText").addEventListener("keydown", function(e){
    if (e.key === "Enter") {
        add();
    }
});

// 마지막 항목 삭제 함수
function lastRemove(){
    if(todoList[0]){
        todoList.pop();
    }else{
        console.log("리스트가 비어있습니다");
    }
    render(todoList);
    saveToLocalStorage();
}

// 첫 항목 삭제 함수
function firstRemove(){
    if(todoList[0]){
        todoList.shift();
    }else{
        console.log("리스트가 비어있습니다");
    }
    render(todoList);
    saveToLocalStorage();
}

// 단일 항목(중간 값) 삭제 함수
function remove(index){
    todoList.splice(index,1);
    render(todoList);
    saveToLocalStorage();
}

// JSON형식으로 서버에 저장(5MB)하는 함수
function saveToLocalStorage() {
    localStorage.setItem('todoList', JSON.stringify(todoList));
}

// 처음 실행할 때 서버에 저장되어 있던 JSON 불러와서 화면에 렌더링
render(todoList);
// // 처음 실행할 때 초기화 후 렌더링
// initTodo();
// render(todoList);