function gugudan(start, end, div){
    let gugu = document.querySelector("#gugu");
    let guguString = '';
    for (let groupStart = start; groupStart <= end; groupStart += div) {
        let groupEnd = Math.min(groupStart + div - 1, end);
        guguString += "<tr>";
        for (let j = groupStart; j <= groupEnd; j++) {
            guguString += `<th colspan="5" style="text-align: center;">${j}단</th>`;
        }
        guguString += "</tr>";
        
        for (let i = 1; i <= 9; i++) {
            guguString += "<tr>";
            for (let j = groupStart; j <= groupEnd; j++) {
                guguString += `<td>${j}</td><td>X</td><td>${i}</td><td>=</td><td class="answer" data-i="${i}" data-j="${j}">
                <input type = "text" class = "inbox">
                <input type = "button" class = "inbtn" value = "확인" onclick = "checkResult(this)">
                </td>`;
            }
            guguString += "</tr>";
        }
        // guguString += "<td></td>";
    }
    gugu.innerHTML = guguString;
}

// 적용하기 버튼을 클릭했을 때 실행되는 이벤트
document.querySelector('#gugu_start').addEventListener("click",()=>{
    let start = parseInt(document.querySelector('#start').value);
    let end = parseInt(document.querySelector('#end').value);
    let div = parseInt(document.querySelector('#div').value);
    gugudan(start,end,div);
});

// 버튼을 눌렀을 때 실행
function checkResult(btn){
    let td = btn.parentElement;
    let input = td.querySelector('.inbox');
    // let result = td.getAttribute('dap');
    let result = td.dataset.i * td.dataset.j;
    if(input.value == result){
        td.style.backgroundColor = "lightgreen";
        input.focus();
    }else{
        td.style.backgroundColor = "red";
        input.value = "";
        input.focus();
    }
}

// inbox에서 엔터를 눌렀을 때 실행
document.querySelector('#gugu').addEventListener('keydown',function(event){
    if(event.target.classList.contains('inbox') && event.key === 'Enter'){
        const td = event.target.closest('td');
        const btn = td.querySelector('.inbtn');
        checkResult(btn);
    }
});