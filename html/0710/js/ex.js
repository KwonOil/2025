// 달력, 컨트롤, 결과 영역 엘리먼트 참조
const calendarEl = document.getElementById("calendar");
const controls = document.getElementById("controls");

const rateSpan = document.getElementById("attendance-rate");
const presentSpan = document.getElementById("present-count");
const absentSpan = document.getElementById("absent-count");
const lateSpan = document.getElementById("late-count");
const earlyLeaveSpan = document.getElementById("early-leave-count");
const vacationLeftSpan = document.getElementById("vacation-left");

// localStorage에서 출석 데이터 불러오기 (없으면 빈 객체)
const attendanceMap = JSON.parse(localStorage.getItem("attendanceMap") || '{}');

// 출석 인정 기간 시작/종료일 (localStorage에서 불러오기)
let attendanceStartDate = localStorage.getItem("attendanceStart") || "";
let attendanceEndDate = localStorage.getItem("attendanceEnd") || "";

// 년도, 월 선택 셀렉트와 출석 인정 기간 입력 생성
const yearSelect = document.createElement("select");
const monthSelect = document.createElement("select");
const startInput = document.createElement("input");
const endInput = document.createElement("input");

startInput.type = "date";
endInput.type = "date";
startInput.value = attendanceStartDate;
endInput.value = attendanceEndDate;

startInput.title = "출석 인정 시작일";
endInput.title = "출석 인정 종료일";

// 출석 인정 시작일 변경 시 처리
startInput.addEventListener("change", () => {
    attendanceStartDate = startInput.value;
    localStorage.setItem("attendanceStart", attendanceStartDate);
    drawCalendar(Number(yearSelect.value), Number(monthSelect.value));
    calculateRate();
});
// 출석 인정 종료일 변경 시 처리
endInput.addEventListener("change", () => {
    attendanceEndDate = endInput.value;
    localStorage.setItem("attendanceEnd", attendanceEndDate);
    drawCalendar(Number(yearSelect.value), Number(monthSelect.value));
    calculateRate();
});

// 오늘 날짜 문자열 (YYYY-MM-DD) 반환
function getTodayStr() {
    const now = new Date();
    return now.toISOString().split("T")[0];
}
// 주어진 날짜가 출석 인정 기간 내인지 체크
function isInPeriod(dateStr) {
    return (!attendanceStartDate || dateStr >= attendanceStartDate) &&
            (!attendanceEndDate || dateStr <= attendanceEndDate);
}
// 주어진 날짜가 오늘 이전 혹은 오늘인지 체크
function isPastOrToday(dateStr) {
    return dateStr <= getTodayStr();
}
// 날짜 문자열 포맷팅 (YYYY-MM-DD)
function formatDateKey(year, month, day) {
    return `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
}
// 두 날짜 사이 개월 수 계산 (휴가 계산에 사용)
function monthsBetween(start, end) {
    const d1 = new Date(start);
    const d2 = new Date(end);
    return d2.getMonth() - d1.getMonth() + 12 * (d2.getFullYear() - d1.getFullYear());
}
// localStorage에 출석 데이터 저장
function saveData() {
    localStorage.setItem("attendanceMap", JSON.stringify(attendanceMap));
}

// 달력 그리기 함수
function drawCalendar(year = new Date().getFullYear(), month = new Date().getMonth()) {
    calendarEl.innerHTML = "";

    // 해당 달의 첫 요일과 마지막 날짜 계산
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();

    const table = document.createElement("table");
    table.className = "calendar-table";

    // 달력 요일 헤더
    const thead = document.createElement("thead");
    thead.innerHTML = `<tr><th>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th>토</th></tr>`;
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    let tr = document.createElement("tr");

    // 첫 주 빈칸 생성
    for (let i = 0; i < firstDay; i++) {
        tr.appendChild(document.createElement("td"));
    }

    // 날짜별 셀 생성
    for (let date = 1; date <= lastDate; date++) {
        const day = new Date(year, month, date).getDay();
        const td = document.createElement("td");
        const dateStr = formatDateKey(year, month + 1, date);

        const container = document.createElement("div");
        container.className = "day-cell";

        const label = document.createElement("div");
        label.textContent = date;
        label.className = "date-label";

        container.appendChild(label);

        if (day !== 0 && day !== 6) {  // 평일일 때만 버튼 그룹 생성
            const btns = ["출석", "결석", "지각", "조퇴", "휴가"];
            const btnContainer = document.createElement("div");
            btnContainer.className = "btn-group";

            btns.forEach(type => {
                const btn = document.createElement("button");
                btn.textContent = type;
                btn.className = "btn";

                if (attendanceMap[dateStr] === type) btn.classList.add("selected");

                if (!isInPeriod(dateStr) || !isPastOrToday(dateStr)) {
                    btn.classList.add("disabled");
                    btn.disabled = true;
                }

                btn.addEventListener("click", () => {
                    if (!isInPeriod(dateStr) || !isPastOrToday(dateStr)) return;

                    if (type === "휴가") {
                        const todayStr = getTodayStr();
                        let totalVacationAllowed = attendanceStartDate ? monthsBetween(attendanceStartDate, todayStr) + 1 : 0;
                        let used = Object.values(attendanceMap).filter(v => v === "휴가").length;
                        if (used >= totalVacationAllowed) {
                            alert("남은 휴가가 없습니다.");
                            return;
                        }
                    }

                    attendanceMap[dateStr] = type;
                    saveData();
                    drawCalendar(year, month);
                    calculateRate();
                });

                btnContainer.appendChild(btn);
            });

            container.appendChild(btnContainer);
        } // else (주말)에는 버튼 그룹 안 만들기

        td.appendChild(container);
        tr.appendChild(td);

        if (day === 6) {
            tbody.appendChild(tr);
            tr = document.createElement("tr");
        }
    }

    // 마지막 줄 추가
    if (tr.children.length > 0) tbody.appendChild(tr);

    table.appendChild(tbody);
    calendarEl.appendChild(table);
}

// 출석률 계산 함수
function calculateRate() {
    const todayStr = getTodayStr();

    let totalDays = 0;
    let presentDays = 0;
    let lateLeaveCount = 0; // 지각+조퇴 횟수
    let vacationUsedCount = 0;
    let absentCount = 0;
    let lateCount = 0; // 지각 횟수
    let earlyLeaveCount = 0; // 조퇴 횟수

    // 저장된 출석 데이터 순회
    for (const dateStr in attendanceMap) {
        if (!isInPeriod(dateStr) || !isPastOrToday(dateStr)) continue;

        const val = attendanceMap[dateStr];
        if (val === "-" || !val) continue;

        const d = new Date(dateStr);
        const w = d.getDay();
        if (w === 0 || w === 6) continue; // 주말 제외

        totalDays++;

        if (val === "출석") {
            presentDays++;
        } else if (val === "결석") {
            absentCount++;
        } else if (val === "지각") {
            presentDays++; // 지각도 출석으로 인정
            lateLeaveCount++;
            lateCount++;
        } else if (val === "조퇴") {
            presentDays++; // 조퇴도 출석으로 인정
            lateLeaveCount++;
            earlyLeaveCount++;
        } else if (val === "휴가") {
            vacationUsedCount++;
        }
    }

    // 지각+조퇴가 3번 이상이면 출석일수 1 감소
    const lateLeavePenalty = lateLeaveCount >= 3 ? 1 : 0;
    const adjustedPresent = Math.max(presentDays - lateLeavePenalty - absentCount, 0);

    // 총 출석 인정일 (평일 - 결석 - 휴가)
    const attendanceDays = totalDays - absentCount - vacationUsedCount;
    const rate = attendanceDays > 0 ? ((adjustedPresent / attendanceDays) * 100).toFixed(1) : "0.0";

    // 허용된 휴가 개월수 계산 및 남은 휴가일수 계산
    let totalVacationAllowed = 0;
    if (attendanceStartDate) {
        totalVacationAllowed = monthsBetween(attendanceStartDate, todayStr);
    }
    let vacationLeft = totalVacationAllowed - vacationUsedCount;
    if (vacationLeft <= 0) vacationLeft = 0;

    // 화면에 결과 출력
    rateSpan.textContent = `${rate}%`;
    presentSpan.textContent = presentDays;
    absentSpan.textContent = absentCount;
    lateSpan.textContent = lateCount;
    earlyLeaveSpan.textContent = earlyLeaveCount;
    vacationLeftSpan.textContent = vacationLeft;
}

// 초기 셋업: 년도/월 선택박스 생성 및 이벤트 연결
(function initYearMonthSelect() {
    const now = new Date();
    const currentYear = now.getFullYear();
    const currentMonth = now.getMonth();

    // 년도 선택 옵션 (현재 연도 기준 -5년 ~ +5년)
    for (let y = currentYear - 5; y <= currentYear + 5; y++) {
        const option = document.createElement("option");
        option.value = y;
        option.textContent = `${y}년`;
        if (y === currentYear) option.selected = true;
        yearSelect.appendChild(option);
    }

    // 월 선택 옵션 (1월 ~ 12월)
    for (let m = 0; m < 12; m++) {
        const option = document.createElement("option");
        option.value = m;
        option.textContent = `${m + 1}월`;
        if (m === currentMonth) option.selected = true;
        monthSelect.appendChild(option);
    }

    // 년도 선택 변경 시 달력 다시 그림
    yearSelect.addEventListener("change", () => {
        drawCalendar(Number(yearSelect.value), Number(monthSelect.value));
    });
    // 월 선택 변경 시 달력 다시 그림
    monthSelect.addEventListener("change", () => {
        drawCalendar(Number(yearSelect.value), Number(monthSelect.value));
    });

    // 라벨 생성
    const labelY = document.createElement("label");
    labelY.textContent = "년도 선택:";
    const labelM = document.createElement("label");
    labelM.textContent = "월 선택:";

    // 컨트롤 박스에 년도/월 선택 요소 삽입
    controls.prepend(monthSelect);
    controls.prepend(labelM);
    controls.prepend(yearSelect);
    controls.prepend(labelY);

    // 출석 인정 기간 입력 박스 추가 (뒤쪽에 배치)
    controls.appendChild(document.createTextNode(" 출석 인정 시작일: "));
    controls.appendChild(startInput);
    controls.appendChild(document.createTextNode(" 출석 인정 종료일: "));
    controls.appendChild(endInput);

    // 최초 달력 렌더링 및 출석률 계산
    drawCalendar(currentYear, currentMonth);
    calculateRate();
})();