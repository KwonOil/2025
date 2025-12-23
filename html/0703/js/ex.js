let tagP = document.querySelectorAll("p");
tagP.forEach((p,i) => p.innerHTML = `변경된 텍스트${i+1}`);

let tagA = document.querySelectorAll("a");
tagA.forEach((a, i) =>{
    if(i % 2 == 0) a.style.backgroundColor = '#ddd';
});

// let classHidden = document.querySelectorAll(".hidden");
// classHidden.forEach((h) => h.style.display = 'none');

let magic = document.querySelector("#magic");
magic.addEventListener("click",() => {
    let classDiv = document.querySelectorAll("div");
    classDiv.forEach((d) => {d.classList.toggle("hidden");})
    // classList.toggle("클래스명"); 클래스 토글
    // classList.add("클래스명"); 클래스 추가
    // classList.remove("클래스명"); 클래스 삭제
});