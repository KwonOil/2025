// 1. if ~ else if ~ else 구문
var x1 = 20, y1 = 20;
document.write("숫자 계산입니다<br>");
if(x1 === y1){
    document.write("x1과 y1는 같습니다.");
}else if(x1 < y1){
    document.write("x1는 y1보다 작습니다.");
}else if(x1 > y1){
    document.write("x1는 y1보다 큽니다.");
}else{
    document.write("???");
}
document.write("<br><br>");

// 2. 삼항연산자
var x2 = 3, y2 = 5;
var result = (x2 > y2) ? x2 : y2;

document.write("x2 = " + x2 + ", y2 = " + y2 + "<br>");
document.write("둘 중에 더 큰 수는 " + result + "입니다.");

document.write("<br><br>");

// 3. 조건문과 비교 연산자
var mathScore = 55, englighScore = 90, scienceScore = 95;

document.write(`수학 : ${mathScore}점, 영어 : ${englighScore}점, 과학 : ${scienceScore}점<br>`);

if(mathScore > 60 && englighScore > 60 && scienceScore > 60){
    document.write("모든 과목에서 통과했습니다.<br>");
}else{
    document.write("어떤 과목에서 통과하지 못했습니다.<br>");
}

if(mathScore >= 80 || englighScore >= 80){
    document.write("영어 혹은 수학에서 우수한 성적을 받았습니다.");
}else{
    document.write("영어 혹은 수학에서 우수한 성적을 받지 못했습니다.");
}
document.write("<br><br>");

// 4. switch ~ case 구문
var x3 = 10;
document.write(typeof x3);
document.write("<br>");

switch(typeof x3){
    case "number":
        document.write("숫자입니다");
        break;
    case "string":
        document.write("문자열입니다");
        break;
    case "object":
        document.write("객체입니다");
        break;
    default:
        document.write("뭔가요 이건?");
}
document.write("<br><br>");

// 4-1. switch ~ case 심화
// var day = prompt("오늘은 무슨 요일인가요?\n(예: 월요일, 화요일 등)");

// switch (day) {
//     case "월요일":
//         document.write("오늘은 새로운 한 주의 시작입니다!<br>운동을 해보세요.");
//         break;
//     case "화요일":
//         document.write("오늘은 좋은 책을 읽는 날입니다.<br>독서 시간을 가져보세요.");
//         break;
//     case "수요일":
//         document.write("중간 주입니다!<br>친구와 커피 한 잔 어때요?");
//         break;
//     case "목요일":
//         document.write("오늘은 요리를 시도해보세요.<br>새로운 레시피를 찾아보세요!");
//         break;
//     case "금요일":
//         document.write("주말이 다가옵니다!<br>영화를 보러 가는 건 어떨까요?");
//         break;
//     case "토요일":
//         document.write("완전한 휴식의 날입니다!<br>가족과 함께 시간을 보내세요.");
//         break;
//     case "일요일":
//         document.write("다음 주를 준비하는 날입니다.<br>일주일 계획을 세워보세요.");
//         break;
//     default:
//         document.write("올바른 요일을 입력해주세요.");
// }
// document.write("<br><br>");

let now = new Date();               // Date()를 객체로 생성
let day = now.getDay();             // 요일(0~6) - 0:일요일
// switch(day){
//     case 0:
//         document.write("다음 주를 준비하는 날입니다.<br>일주일 계획을 세워보세요.");
//         break;
//     case 1:
//         document.write("오늘은 새로운 한 주의 시작입니다!<br>운동을 해보세요.");
//         break;
//     case 2:
//         document.write("오늘은 좋은 책을 읽는 날입니다.<br>독서 시간을 가져보세요.");
//         break;
//     case 3:
//         document.write("중간 주입니다!<br>친구와 커피 한 잔 어때요?");
//         break;
//     case 4:
//         document.write("오늘은 요리를 시도해보세요.<br>새로운 레시피를 찾아보세요!");
//         break;
//     case 5:
//         document.write("주말이 다가옵니다!<br>영화를 보러 가는 건 어떨까요?");
//         break;
//     case 6:
//         document.write("완전한 휴식의 날입니다!<br>가족과 함께 시간을 보내세요.");
//         break;
// }

switch(day){
    case 1:
    case 2:
    case 3:
    case 4:
        document.write("아직도 주말은 멀었습니다!!!");
        break;
    case 5:
        document.write("내일은 주말입니다.");
        break;
    case 6:
        document.write("주말 시작!");
        break;
    case 0:
        document.write("주말 끝...");
        break;
    default:
        document.write("???");
}