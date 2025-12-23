const number = RandomInt(1,100);
cprint(number);
let attemps = 5;
while(attemps > 0){
    const input = prompt(`1~100 사이의 숫자를 입력하세요(남은기회 : ${attemps}회)`);
    if(!input) break;
    if(input == number){
        alert("정답입니다!😘")
        break;
    }else{
        attemps--;
        if(input > number){
            alert("입력값은 정답보다 더 큽니다")
        }else{
            alert("입력값은 정답보다 더 작습니다")
        }
    }
    if(attemps == 0){
        alert(`정답은 ${number}였습니다`)
    }
}