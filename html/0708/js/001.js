// 코드의 재사용을 가능하게 하고, 특정 작업을 수행하는 독립적인 블록
function addNum(x, y){
    return (x + y);
}
function greeting(name){
    return name + "님 안녕하세요";
}
function print(value = "", sep = "<br>"){
    document.write(value + sep);
}

// function cprint(value = ""){
//     document.write(value);
// }
function cprint(...args){
    document.write(...args);
}

let result1 = addNum(3,5);
let result2 = addNum(5,8);
// print(result1+" / "+result2);

let a = greeting("홍길동");
// print(a);

// 함수 표현식(익명함수)
let sqr2 = function(x,y){
    return x ** y;
}
// print(sqr2(3,4));

// 화살표 함수
let sqr3 = (x,y) => { return x ** y };
// print(sqr3(3,4));