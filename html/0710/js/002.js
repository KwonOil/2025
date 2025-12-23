// const arr = [3, 1, 4, 2];
// const strArr = ["banana","apple","cherry"];

// // 1. sort() : 오름차순 정렬
// arr.sort();
// strArr.sort();
// cprint(arr, strArr);

// // sort() : 내림차순 정렬
// arr.sort((a,b) => b-a);
// strArr.sort((a,b) => b-a);
// cprint(arr, strArr);

// // 3. reverse() : 배열 요소를 역순으로 재정렬
// arr.reverse();
// strArr.reverse();
// cprint(arr, strArr);

// // 4. find : 배열의 요소를 하나씩 검사하여, 조건을 만족하는 첫 번째 요소를 반환
// const arr = [5, 12, 8, 130, 44];
// const found = arr.find(num => num > 10);
// // 5. findIndex : ~, 조건을 만족하는 첫 번째 요소의 인덱스를 반환
// const index = arr.findIndex(num => num > 10);
// // 6. filter : ~, 조건을 만족하는 모든 요소를 반환
// const found2 = arr.filter(num => num > 10);
// cprint(found);
// cprint(index);
// cprint(found2);

// // 7. includes : 배열의 특정 요소를 포함하고 있는지 체크해 반환
// const arr1 = [1,"2",3];
// cprint(arr1.includes(2));
// cprint(arr1.includes(4));

// // 8. fill(x) : 배열의 모든 요소를 x로 채운다
// const arr = new Array(5).fill(0);
// cprint(arr);

// // 5칸짜리 빈 배열 생성
// const arr1 = new Array(5);
// cprint(arr1);

// // 값이 5인 한칸짜리 배열 생성
// const arr2 = Array.of(5);
// cprint(arr2);

// // 값이 5,6인 두칸짜리 배열 생성
// const arr3 = new Array(5, 6);
// cprint(arr3);

// // 값이 5,6,7인 세칸짜리 배열 생성
// const arr4 = [5, 6, 7];
// cprint(arr4);

// every() : 배열의 모든 요소를 돌면서 콜백함수를 실행하고 실행 결과가 모두 참이라면 true, 하나라도 거짓이 있으면 false를 반환한다
// some()) : 배열의 모든 요소를 돌면서 콜백함수를 실행하고 실행 결과가 하나라도 참이라면 true, 모두 거짓이면 false를 반환한다
let arr = [-10, 5, -20, 4];
function compareValue(value){
    return value < 5;
}
cprint(arr.every(compareValue));
cprint(arr.some(compareValue));