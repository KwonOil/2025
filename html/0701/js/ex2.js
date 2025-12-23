// 사용자가 입력한 주차 시간을 기반으로 총 주차 요금을 계산하는 프로그램을 작성하시오.
// 2시간 이하일 경우 5000원, 2시간 초과 시 추가로 3000원씩 부과하시오.
// 계산된 요금을 출력하시오.
var time = prompt("주차시간을 입력하세요(시간)");
let onehour = 60 * 60;

time = time * onehour;
let t0 = 2 * onehour;
let pay = 5000, pluspay = 3000;

document.write(`주차시간 : ${time}초<br>`);
if(time > t0){
    time -= t0;
    t1 = parseInt((time - 1) / onehour) + 1;
    // document.write(`t1 ${t1}원입니다<br>`);
    pay = pay + t1 * pluspay;
}
document.write(`주차요금은 ${pay}원입니다`);