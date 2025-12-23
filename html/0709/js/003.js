let today = new Date();

// 특정 날짜 : 년, 월, 일, 시, 분, 초
let date1 = new Date(2025, 7-1, 9, 12, 0, 0);
// 특정 날짜 : ISO 8601 형식
let date2 = new Date('2023-10-27');
let date3 = new Date('2025-07-09T12:00:00');

// 특정 날짜 : 타임스탬프(밀리초)
today.getTime(); // 1970년 1월 1일 00:00:00부터 현재까지의 밀리초
let date4 = new Date(1752042260000);

function formatDate(date) {
    const year = date.getFullYear();
    // 월은 0부터 시작하므로 + 1
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

setInterval(()=>{
    document.querySelector("#ctime").textContent = formatDate(date4);
},1000);
