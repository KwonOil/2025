// 0. data 설정
let scores = [
    [90, 92, 75, 90, 88], // 국어
    [81, 78, 98, 88, 90], // 영어
    [95, 75, 98, 80, 93], // 수학
    [90, 100, 80, 90, 80]  // 과학
]
let classes = ['국어','영어','수학','과학'];
let names = ['권오일','이현민','이세은','구윤서','정인회']

// 1. 각 과목별 총점과 평균 구하기
// 총점 구해서 배열 반환
function sumScore(scores){
    let total_class = [];
    scores.forEach((score_class)=>{total_class.push(score_class.reduce((acc, score) => (acc + score), 0));});
    // console.log(total_class);
    return total_class;
}

// 평균 구해서 배열 반환
function avgScore(scores){
    let avg_class = [];
    let total_class = sumScore(scores);

    for(let i = 0; i < scores.length; i++){
        avg_class.push((total_class[i] / scores[i].length).toFixed(1));
    }
    // console.log(avg_class);
    return avg_class;
}

// 배열에 따른 총점, 평균 HTML로 출력
function printScore(scores, arrays){
    let resultString = '';
    resultString+=("<p>");
    resultString+=("<hr>SCORES<br>");
    for(let i = 0; i < scores.length; i++){
        resultString+=(`${arrays[i]} : `);
        for(let j = 0; j < scores[i].length; j++){
            resultString+=(scores[i][j]);
            if(j < scores[i].length - 1)
                resultString+=(", ");
        }
        resultString+=("<br>");
    }
    resultString+=("<hr>");
    for(let i = 0; i < scores.length; i ++){
        resultString+=(`${arrays[i]} 총점 : ${sumScore(scores)[i]}점<br>`);
        resultString+=(`${arrays[i]} 평균 : ${avgScore(scores)[i]}점<br><hr></p>`);
    }
    // console.log(resultString);
    return resultString;
}

// 2. 각 학생별 성적 총점과 평균 구하기
// 행 열 치환하기
function transpose(matrix) {
    return matrix[0].map((_, colIndex) => matrix.map(row => row[colIndex]));
}

// 입력값 체크
function checkInput(inputs){
    for(let i = 0; i < inputs.length; i++){
        if(inputs[i].value === ""){
            document.querySelector('#print').innerHTML = "빈 칸이 있습니다<br>"
            return false;
        }
    }
    for(let i = 1; i < inputs.length; i++){
        if(inputs[i].value < 0 || inputs[i].value > 100){
            document.querySelector('#print').innerHTML = "점수를 확인하세요<br>"
            return false;
        }
    }
    return true;
}
// 성적 입력 버튼 클릭
function inputScore(e){
    let div = e.parentElement;
    let inputs = div.querySelectorAll('input');
    if(checkInput(inputs)){
        for(let i = 0; i < inputs.length; i++){
            if(i == 0){
                names.push(inputs[i].value);
            }
            else{
                scores[i-1].push(parseInt(inputs[i].value));
            }
            inputs[i].value = "";
        }
        document.querySelector('#print').innerHTML = "성적 입력 완료";
    }else{
        document.querySelector('#print').innerHTML += "다시 입력하세요!";
    }
    // console.log(names);
    // console.log(scores);
}
// 과목별 점수 보기 버튼 클릭
function printClassScore(scores, arrays){
    document.querySelector('#print').innerHTML = printScore(scores,arrays);
}
// 학생별 점수 보기 버튼 클릭
function printStudentScore(scores, arrays){
    document.querySelector('#print').innerHTML = printScore(transpose(scores),arrays);
}