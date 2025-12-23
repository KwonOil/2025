function convertCurrency(){
    let currency = {
        usd : 1.3526,
        eur : 1.59634,
        jpy : 0.94301,
        cnh : 0.18902
    }
    let amount = parseInt(document.getElementById("amount").value);
    let input_cur = document.getElementById("currency").value;
    let input_str = '';
    let result = amount * currency[input_cur] / 1000;

    result = result.toLocaleString('ko-KR', {minimumFractionDigits : 1, maximumFractionDigits: 2});
    amount = amount.toLocaleString();

    switch(input_cur){
        case 'usd':
            input_str = '미국'
            result += '달러'
            break;
        case 'eur':
            input_str = '유럽'
            result += '유로'
            break;
        case 'jpy':
            input_str = '일본'
            result += '엔'
            break;
        case 'cnh':
            input_str = '중국'
            result += '위안'
            break;
    }
    console.log(input_cur);
    document.getElementById("conversionResult").innerHTML = `<span style = "color:blue">한국 돈 <b>${amount}원</b></span>은 <span style = "color:red">${input_str} 돈으로 <b>${result}</b></span>입니다`;
}