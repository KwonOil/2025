// let arrList1 = [1,true,"JavaScript"];
// let arrList2 = new Array(1,true,"javaScript");
// console.log(arrList1, arrList2);

// arrList1[arrList1.length] = "HTML";
// arrList2.push("HTML");
// console.log(arrList1, arrList2);

// console.log(arrList1, arrList2);

//1. push()
//배열의 끝에 요소를 추가합니다.
let fruits = ['apple', 'banana'];
fruits.push('cherry'); // ['apple', 'banana', 'cherry']
console.log(fruits);

//2. pop()
//배열의 마지막 요소를 제거하고 반환합니다.
let numbers = [1, 2, 3];
let lastNumber = numbers.pop(); // lastNumber는 3
console.log(numbers,"numbers.pop :", lastNumber); // [1, 2]

//3. shift()
//배열의 첫 번째 요소를 제거하고 반환합니다.
let colors = ['red', 'green', 'blue'];
let firstColor = colors.shift(); // firstColor는 'red'
console.log(colors,"colors.shift : " +firstColor); // ['green', 'blue']

//4. unshift()
//배열의 시작 부분에 요소를 추가합니다.
let animals = ['dog', 'cat'];
animals.unshift('rabbit'); // ['rabbit', 'dog', 'cat']
console.log(animals);

//5. splice()
//배열의 특정 위치에서 요소를 추가하거나 제거합니다.
let numbers2 = [1, 2, 3, 4, 5];
numbers2.splice(2, 1, 10); // 인덱스 2에서 1개 요소를 제거하고 10을 추가
console.log(numbers2); // [1, 2, 10, 4, 5]

//6. slice()
//배열의 특정 부분을 잘라내어 새로운 배열을 반환합니다.
let fruits2 = ['apple', 'banana', 'cherry', 'date'];
let citrus = fruits2.slice(1, 3); // 인덱스 1부터 3까지 잘라냄
console.log(fruits2, citrus); // ['banana', 'cherry']

//7. forEach()
//배열의 각 요소에 대해 제공된 함수를 실행합니다.
let numbers3 = [1, 2, 3];
numbers3.forEach((num) => {
    console.log(num * 2); // 2, 4, 6 출력
});

let numbers4 = [1, 2, 3]; 
numbers4.forEach(function(num) { 
    console.log(num * 2); // 2, 4, 6 출력 
});

//8. map()
//각 요소에 대해 주어진 함수를 호출하고, 그 결과로 새로운 배열을 생성합니다.
let numbers5 = [1, 2, 3];
let doubled = numbers5.map((num) => (num * 2)); // [2, 4, 6]
console.log(doubled);

//9. filter()
//주어진 조건을 만족하는 요소들로 새로운 배열을 생성합니다.
let numbers6 = [1, 2, 3, 4, 5];
let evenNumbers = numbers6.filter((num) => (num % 2 === 0)); // [2, 4]
console.log(evenNumbers);

//10. reduce()
//배열을 단일 값으로 축약하는 데 사용됩니다.
let numbers7 = [1, 2, 3, 4];
let sum = numbers7.reduce((acc, num) => (acc + num), 0); // 10
console.log(sum);