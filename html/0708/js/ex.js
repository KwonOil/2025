let scores = [80, 95, 90, 87, 93];

function sum(scores){
    return scores.reduce((acc, score) => (acc + score), 0);
}
function avg(scores){
    return sum(scores)/scores.length;
}

// print2("Sum : ", sum(scores),"<br>");
// print2("Average : ", avg(scores));

let todoList = [];

// todoList.push("공부");
// todoList.push("청소");
// todoList.push("점심");
// todoList.push("면접");

cprint("현재 배열 : ", todoList);

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

// render(todoList);

function add(){
    let inputText = document.querySelector("#inputText");
    let newItem = inputText.value;
    inputText.value = "";
    if(newItem){
        todoList.push(newItem);
    }
    render(todoList);
}

document.querySelector("#inputText").addEventListener("keydown", function(e){
    if (e.key === "Enter") {
        add();
    }
});

function lastRemove(){
    if(todoList[0]){
        todoList.pop();
    }else{
        console.log("리스트가 비어있습니다");
    }
    render(todoList);
}

function firstRemove(){
    if(todoList[0]){
        todoList.shift();
    }else{
        console.log("리스트가 비어있습니다");
    }
    render(todoList);
}

function remove(index){
    todoList.splice(index,1);
    render(todoList);
}