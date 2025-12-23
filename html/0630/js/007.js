for(let i = 1; i <= 10; i++){
    console.log(i);
}
var x = 10, y = 10;
document.write("x : " + x + ", y : " + y + "<br>");
document.write("(++x - 3) : " + (++x - 3) + "<br>");
// x의 값을 우선 1 증가시킨 후에 3을 뺌.
document.write("x : " + x + "<br>");
// 11
document.write("(y++ - 3) : " + (y++ - 3) + "<br>");
// 먼저 y에서 3을 뺀 후에 y의 값을 1 증가시킴.
document.write("y : " + y);
// 11

// 비교 연산자 예제
let a = 5;
let b = '5';
let c = 10;

console.log(a == b);  // true (값이 같음)
console.log(a === b); // false (타입이 다름)
console.log(a != c);  // true (값이 다름)
console.log(a !== b); // true (값은 같지만 타입이 다름)
console.log(a > c);   // false (5는 10보다 작음)
console.log(a >= 5);  // true (같음)
console.log(a < c);   // true (5는 10보다 작음)
console.log(a <= 5);  // true (같음)

// 논리 연산자 예제
let x2 = true;
let y2 = false;

console.log(x2 && y2); // false (모두 참이 아님)
console.log(x2 || y2); // true (하나가 참)
console.log(!x2);     // false (x가 참이므로 NOT 연산)
console.log(!(x2 && y2)); // true (AND 결과가 거짓이므로 NOT 연산)