let fruit = ['사과','배','복숭아','수박','참외','메론'];


// let i = 0;
// while(i < fruit.length){
//     if(fruit[i] === '수박'){
//         i++;
//         continue;
//     }
//     document.writeln(fruit[i] + "<br>");
//     i++
// }

// 기본 for문
for(let j = 0; j < fruit.length; j++){
    if(fruit[j] === '수박'){
        continue;
    }
    document.writeln(`<p class = "r">${fruit[j]}<br></p>`);
}
document.writeln("<br>");

// in을 활용할 for문(객체의 키를 가져오기 때문에 비추)
for(let j in fruit){
    document.writeln(`<p class = "r"> j in fruit : ${j}<br></p>`);
}
document.writeln("<br>");

// of를 활용한 for문(이터러블 객체의 값을 가져옴)
for(let j of fruit){
    document.writeln(`<p class = "g">j of fruit : ${j}<br></p>`);
}
document.writeln("<br>");

// forEach
fruit.forEach(function(value, index){
    document.writeln(`<p class = "r">forEach - index : ${index}, value : ${value}<br></p>`);
});
document.writeln("<br>");