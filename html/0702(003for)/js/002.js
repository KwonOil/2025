// let i = 1;
// while(i <= 10){
//     document.write(`${i * 5}<br>`);
//     i++;
// }
// document.write("출력 끝")

// let i = 1, j = 1;

// while(i > 3){
//     document.write(`${i}<br>`);
// }

// do{
//     document.write(`${j}<br>`);
// }
// while(j > 3);

// let password;
// do{
//     password = prompt("비밀번호를 입력하세요( 최소 6자 )")
// }while(password.length < 6);

// document.write("패스워드 : " + password);

let i = 1, save = 3;
while(i < 10){
    document.write(save + "<br>");
    save--;
    i++;
    if(save == 0) break;
}