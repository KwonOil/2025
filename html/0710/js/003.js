// let randomNum1 = Math.random();
// cprint(randomNum1);
// let randomNum2 = Math.random() * 10;
// cprint(randomNum2);
// let randomNum3 = Math.floor(Math.random() * 100);
// cprint(randomNum3);
// let randomNum4 = 5 + Math.floor(Math.random() * 8);
// cprint(randomNum4);
// function getRandomInt(min, max){
//     return Math.floor(Math.random() * (max - min + 1)) + min;
// }
// cprint(RandomInt(1,45));

const paths = ['A','B','C','D'];
// const SelectedPath = paths[Math.floor(Math.random() * paths.length)]
const SelectedPath = paths[RandomInt(0,paths.length-1)];
cprint(SelectedPath);