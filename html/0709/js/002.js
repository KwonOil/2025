let today = new Date();
function formatDate(date) {
    const year = date.getFullYear();
    // 월은 0부터 시작하므로 + 1
    // const month = String(date.getMonth() + 1).padStart(2, '0');
    let preMonth = 12;
    const month = preMonth < 10 ? '0' + preMonth : ''+preMonth;
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    const milis = String(date.getMilliseconds()).padStart(3);

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milis}`;
}
// document.querySelector("#ctime").textContent = formatDate(today);

// (1000)ms(1초) 마다 function을 반복 실행
setInterval(()=>{
    document.querySelector("#ctime").textContent = formatDate(new Date());
},1000);

// (2000)ms(2초)마다 function을 한번 실행
setTimeout(() => {
    document.querySelector("#ctime2").textContent = formatDate(new Date());
},2000);