let fruit = ['사과','배','복숭아','수박','참외','메론'];

for(let i = 0; i < fruit.length; i++){
    document.getElementById("numberList").innerHTML += `<li>${fruit[i]}</li>`;
}
document.getElementById("numberList").innerHTML += "<br>";

for(let i in fruit){
    document.getElementById("numberList").innerHTML += `<li>${fruit[i]}</li>`;
}
document.getElementById("numberList").innerHTML += "<br>";

for(let i of fruit){
    document.getElementById("numberList").innerHTML += `<li>${i}</li>`;
}
document.getElementById("numberList").innerHTML += "<br>";

fruit.forEach(function(value, index){
    document.getElementById("numberList").innerHTML += `<li>${index + 1} : ${value}</li>`;
});
document.getElementById("numberList").innerHTML += "<br>";

let colors = ['red','green','blue','yellow','purple','coral','aqua','aquamarine','gray'];

colors.forEach((color,index) => {
    document.getElementById('colorButton').innerHTML += `<p><button style = 'background-color : ${color};'>${index} : ${color}</button></p>`;
});