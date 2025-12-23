function generateCalendar(date) {
    const monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]; // 각 월의 일 수
    const now = new Date(date);
    const year = now.getFullYear();
    const month = now.getMonth(); // 0부터 시작
    let daysInMonth = monthDays[month];

    document.querySelector('#title').innerHTML = `<h1>${year}년 ${month+1}월의 달력</h1>`;
    // 윤년 체크 (2월)
    if (month === 1 && ((year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0))) {
        daysInMonth = 29; // 윤년이면 29일
    }

    const firstDay = new Date(year, month, 1);
    const firstDayOfWeek = firstDay.getDay(); // 첫 날의 요일

    // 날짜 배열 생성
    let daysArray = [];
    for (let day = 1; day <= daysInMonth; day++) {
        daysArray.push(day);
    }

    let calendar = '<table><tr><th>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th>토</th></tr>';
    calendar += '<tr>';

    // 첫 주의 빈 칸 추가
    for (let i = 0; i < firstDayOfWeek; i++) {
        calendar += '<td></td>'; // 빈 칸
    }

    // 날짜 추가
    for (let i = 0; i < daysArray.length; i++) {
        if ((i + firstDayOfWeek) % 7 === 0) {
            calendar += '</tr><tr>'; // 주가 끝나면 줄바꿈
        }
        calendar += `<td>${daysArray[i]}</td>`;
    }

    // 마지막 주의 빈 칸 추가
    const lastDayOfWeek = (daysArray.length + firstDayOfWeek) % 7;
    for (let i = lastDayOfWeek; i < 7 && lastDayOfWeek !== 0; i++) {
        calendar += '<td></td>'; // 빈 칸
    }

    calendar += '</tr></table>';
    document.querySelector('#calendar').innerHTML = calendar;
}

document.querySelector('#checkButton').addEventListener('click',() => {
    generateCalendar(document.querySelector('#dateInput').value);
});