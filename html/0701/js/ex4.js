function evaluateScore(){
    let score = document.getElementById("score").value;
    let score_s = '';

    if(score > 100 || score < 0){
        document.getElementById("evaluationResult").innerHTML = `<h3>0 ~ 100 사이의 값을 입력하세요</h3>`;
        return;
    }
    else if(score >= 97) score_s = 'A+';
    else if(score >= 94) score_s = 'A0';
    else if(score >= 90) score_s = 'A-';
    else if(score >= 87) score_s = 'B+';
    else if(score >= 84) score_s = 'B0';
    else if(score >= 80) score_s = 'B-';
    else if(score >= 77) score_s = 'C+';
    else if(score >= 74) score_s = 'C0';
    else if(score >= 70) score_s = 'C-';
    else if(score >= 67) score_s = 'D+';
    else if(score >= 64) score_s = 'D0';
    else if(score >= 60) score_s = 'D-';
    else if(score >=  0) score_s = 'F';
    else{
        document.getElementById("evaluationResult").innerHTML = `???????`;
        return;
    }
    document.getElementById("evaluationResult").innerHTML = `<h1>점수 ${score}점의 성적은 ${score_s}입니다</h1>`;
}