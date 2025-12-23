const array2D = [
                    ['이름', '나이', '도시'],
                    ['홍길동', 25, '서울'],
                    ['김영희', 30, '부산'],
                    ['이철수', 28, '대구']
                ];

console.log("array2D : ", array2D);
// JSON.stringify 객체를 문자열로 변환
const jsonString = JSON.stringify(array2D);
console.log("jsonString : ", jsonString);


const jsonString2 = `[
    {"이름": "홍길동", "나이": 25, "도시": "서울"},
    {"이름": "김영희", "나이": 30, "도시": "부산"},
    {"이름": "이철수", "나이": 28, "도시": "대구"}
]`;

console.log("jsonString2 : ", jsonString2);
// JSON.parse : 문자열을 객체로 변환
const jsonObject = JSON.parse(jsonString2);
console.log("jsonObject : ", jsonObject);

const firstPerson = jsonObject[0];
const name = firstPerson.이름;
const age = firstPerson.나이;
const city = firstPerson.도시;
const result = `첫 번째 사람의 정보:\n이름: ${name}\n나이: ${age}\n도시: ${city}`;

console.log(result);
