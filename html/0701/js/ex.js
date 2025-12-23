// 사용자에게 기온을 입력받고 적절한 옷차림을 추천하는 프로그램
// 20도 이상 : 반팔을 입으세요
// 20도 미만 : 긴팔을 입으세요
var temperature = prompt("기온을 입력하세요");

document.write(`입력받은 현재 온도 : ${temperature}ºC<br>`);

if(temperature >= 20){
    document.write("반팔을 입으세요.");
}else if(temperature < 20){
    document.write("긴팔을 입으세요.");
}