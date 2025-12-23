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
                guguString += `<td>${j}</td><td>X</td><td>${i}</td><td>=</td><td class="answer" data-i="${i}" data-j="${j}">??</td>`;
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

// id가 gugu인 태그를 클릭 시 실행하는 이벤트
document.querySelector("#gugu").addEventListener("click", (e) => {
    // classList.contains("클래스명") : 클래스가 있는지 확인 (true 또는 false)
    if (e.target.classList.contains("answer")) { // 클릭된 타겟의 클래스 중에 answer가 있다면 실행 => 클래스가 answer인 태그를 클릭했을 때 실행
        const i = parseInt(e.target.dataset.i);
        const j = parseInt(e.target.dataset.j);
        e.target.innerHTML = `${i * j}`;
    }
});
