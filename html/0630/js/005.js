// 상수
const y = 3;

// 변수
var n = 1;

let num = 10;
let integer = 20; // 정수
let float = 3.14; // 실수

// 문자열
let firstStr = "안녕하세요";
let secondStr = '안녕하세요';
let thirdStr = `안녕하세요`;
let forthStr = "내 이름은 '홍길동'입니다.";
let fifthStr = '내 이름은 "홍길동"입니다.';
let sixthStr = "내 이름은 \"홍길동\"입니다.";

let strs = firstStr + ". " + forthStr;
console.log(strs);
let strs2 = `${firstStr}. ${forthStr}`;
console.log(strs2);

let vars = num + firstStr;
console.log(vars);

let vars2 = num + integer;
console.log(vars2);

let oneNum = 1;
let twoNum = 2;

document.querySelector("#str").innerHTML = "strs2 : " + strs2;
document.querySelector("#result").innerHTML = "vars2 : " + vars2;
document.querySelector("#result2").innerHTML = "oneNum == twoNum : " + (oneNum == twoNum);
document.querySelector("#result3").innerHTML = "10의 자료형 : " + (typeof 10) + "<br>";
document.querySelector("#result3").innerHTML += `"문자열"의 자료형 : ` + (typeof "문자열") + "<br>";
document.querySelector("#result3").innerHTML += "vars의 자료형 : " + (typeof vars) + "<br>";

