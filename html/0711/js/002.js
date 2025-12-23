const people = [
    { "이름" : "홍길동", "나이" : 25, "도시" : "서울" },
    { "이름" : "김영희", "나이" : 30, "도시" : "부산" },
    { "이름" : "이철수", "나이" : 28, "도시" : "대구" },
    { "이름" : "이철수", "나이" : 38, "도시" : "대전" }
];

document.getElementById('searchButton').onclick = function(){
    // cprint(document.getElementById('nameInput').value);
    const inputName = document.getElementById("nameInput").value;
    const person = people.find(p => p.이름 == inputName);

    let result = "";

    if(person){
        result += `이름 : ${person.이름}\n나이 : ${person.나이}\n도시 : ${person.도시}\n\n`;
    }else{
        result += '검색결과가 없습니다';
    }
    document.getElementById('result').textContent = result;
};