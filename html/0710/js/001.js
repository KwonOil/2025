// // 1. 문자열 길이
// let str1 = "Hello, World!!!";
// cprint(str1.length);

// let str2 = "한글 사랑";
// cprint(str2.length);

// let str3 = "";
// cprint(str3.length);

// // 2. 문자열 체크하기
// let str = "안녕하세요, 자바스크립트!";
// // includes : 문자열이 포함되어 있는지 여부 체크, (인덱스부터)
// cprint(`str : ${str}`);
// cprint(`str.includes("자바", 7) : ` + str.includes("자바", 7));
// cprint(`str.includes("안녕", 1) : ` + str.includes("안녕", 1));

// // 3. startsWith : 특정 문자열로 시작하는지 여부 체크
// cprint(`str.startsWith("안녕") " ` + str.startsWith("안녕"));
// // 4. endsWith : 특정 문자열로 끝나는지 여부 체크
// cprint(`str.endsWith("스크립트!") : ` + str.endsWith("스크립트!"));

// // 5. 문자열 치환(일치되는 모든 문자열 대상)
// let str = "Hello, World!!, World!!";
// cprint(str);
// let newStr = str.replace("World","JavaScript");
// cprint(newStr);
// let newStr2 = str.replaceAll("World","JavaScript");
// cprint(newStr2);

// // 6. split : 구분자를 기준으로 나누기
// const str = "apple,banana,banana,cherry";
// cprint(str);
// const fruits = str.split(",");
// cprint(fruits);
// // 7. join : 특정 구분자로 합쳐서 문자열 만들기
// const result = fruits.join(" - ");
// cprint(result);

// // 8. toUpperCase,toLowerCase : 대문자로 변환, 소문자로 변환
// const str1 = "\tJavaScript\t\n";
// cprint(str1.toUpperCase());
// cprint(str1.toLowerCase());

// // 9. trim() : 좌우 공백제거
// cprint(str1.trim());

// // 10. indexOf : 특정 문자열이 몇번째 인덱스에 존재하는지 검색해서 인덱스 반환
// const str = "Hello, World";
// cprint(str.indexOf("World"));
// // 특정 인덱스부터 검색할 수도 있다. 없으면 -1 반환
// cprint(str.indexOf("World", 10));

// // 11. slice : 시작 인덱스부터 종료 인덱스 바로 앞까지의 문자열을 추출해 반환
// const str = "Hello, World";
// const part1 = str.slice(0,5);
// cprint(part1);
// const part2 = str.slice(7);
// cprint(part2);

// 12. concat : 문자열 합치기
const str1 = "Hello, ";
const str2 = "World";
const result = str1.concat(str2);
cprint(result);