const people = [
    { "이름" : "홍길동", "나이" : 25, "도시" : "서울" },
    { "이름" : "김영희", "나이" : 30, "도시" : "부산" },
    { "이름" : "이철수", "나이" : 28, "도시" : "대구" },
];

cprint(people);
print2(people[0].이름);

function showPerson(idx){
    const person = people[idx];
    const name = person.이름;
    const age = person.나이;
    const city = person.도시;

    const result = `[사람 정보]\n이름 : ${name}\n나이 : ${age}\n도시 : ${city}`;
    document.getElementById('result').textContent = result;
}

document.getElementById('accessButton').onclick = function(){
    showPerson(1);
};