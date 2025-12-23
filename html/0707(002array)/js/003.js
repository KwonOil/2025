let arr = new Array(3);
// console.log(arr.length,arr[0]);

for(let row = 0; row < arr.length; row++){
    arr[row] = new Array(4);
    for(let column = 0; column < arr[row].length; column++){
        arr[row][column] = "[" + row + "," + column + "]";
        document.write(arr[row][column] + " ");
    }
    document.write("<br>");
}
let matrix = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

for (let i = 0; i < matrix.length; i++){
    for (let j = 0; j < matrix[i].length; j++){
        console.log(matrix[i][j]);
    }
}

const obj = {
    name : "Alice",
    age : 25
};

document.write(obj.name + "<br>");
document.write(obj["name"] + "<br>");

const arrayWithObjects = [
    { key1 : 'value1'},
    { key2 : 'value2'}
]

document.writeln(arrayWithObjects[0]["key1"]);
document.writeln(arrayWithObjects[1]["key2"]);
arrayWithObjects[2] = {key3 : 'value3'};
document.writeln(arrayWithObjects[2]["key3"]);
arrayWithObjects[3] = {key4 : 'value4'};
document.writeln(arrayWithObjects[3]["key4"]);
document.writeln("<br><br>");

let scores = [85, 92, 76, 88, 90];

function addScore(score){
    scores.push(score);
}

function removeScore(scores, index){
    if(0 <= index && index < scores.length)
        scores.splice(index,1);
    else
        document.writeln("잘못된 인덱스입니다<br>");
}

function sumScore(scores){
    // let result = 0;
    // scores.forEach((i) => {
    //     result += i;
    // });
    // return result;
    return scores.reduce((acc, score) => (acc + score), 0); // reduce를 통한 간단한 증감연산
}

function avgScore(scores){
    return sumScore(scores) / scores.length;
}

function printScore(scores){
    document.writeln("scores :");
    scores.forEach((score)=>{
        document.writeln(score+" ");
    });
    document.writeln("<br>");
    document.writeln("합계 : "+sumScore(scores)+"점, 평균 : "+avgScore(scores).toFixed(2)+"점<br>");
    document.writeln("<hr>");
}

printScore(scores);
addScore(98);
printScore(scores);
removeScore(scores, 2);
printScore(scores);