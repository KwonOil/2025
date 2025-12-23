document.addEventListener('DOMContentLoaded', () => {
    // DOM 요소
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    const generateBtn = document.getElementById('generateCalendar');
    const calendarContainer = document.getElementById('calendar-container');
    const dayPopup = document.getElementById('day-popup');

    // 데이터 저장 변수
    let attendanceData = {};
    let startDate, endDate;
    let selectedDayElement = null;

    // 이벤트 리스너 설정
    generateBtn.addEventListener('click', initializeCalendar);
    calendarContainer.addEventListener('click', handleDayClick);
    dayPopup.addEventListener('click', handleStatusChange);
    document.addEventListener('click', (e) => { // 팝업 외 영역 클릭 시 닫기
        if (!dayPopup.contains(e.target) && e.target.closest('.day') !== selectedDayElement) {
            hidePopup();
        }
    });

    /** 팝업 숨기기 및 선택 해제 */
    function hidePopup() {
        dayPopup.style.display = 'none';
        if (selectedDayElement) {
            selectedDayElement.classList.remove('selected');
            selectedDayElement = null;
        }
    }

    /** 달력 초기화 및 생성 */
    function initializeCalendar() {
        if (!startDateInput.value || !endDateInput.value) {
            alert('시작일과 종료일을 모두 선택해주세요.');
            return;
        }
        startDate = new Date(startDateInput.value);
        endDate = new Date(endDateInput.value);
        startDate.setHours(0, 0, 0, 0);
        endDate.setHours(0, 0, 0, 0);

        if (startDate > endDate) {
            alert('시작일은 종료일보다 이전이어야 합니다.');
            return;
        }

        attendanceData = {};
        hidePopup();
        renderCalendar();
        updateStatsDisplay();
    }

    /** 달력 렌더링 */
    function renderCalendar() {
        calendarContainer.innerHTML = '';
        let currentMonth = new Date(startDate.getFullYear(), startDate.getMonth(), 1);

        while (currentMonth <= endDate) {
            const monthGrid = createMonthGrid(currentMonth.getFullYear(), currentMonth.getMonth());
            calendarContainer.appendChild(monthGrid);
            currentMonth.setMonth(currentMonth.getMonth() + 1);
        }
    }

    /** 특정 월의 그리드 생성 */
    function createMonthGrid(year, month) {
        const monthContainer = document.createElement('div');
        monthContainer.className = 'month-grid';
        monthContainer.innerHTML = `<h2 class="month-header">${year}년 ${month + 1}월</h2>`;

        const grid = document.createElement('div');
        grid.className = 'calendar-grid';
        const weekdays = ['일', '월', '화', '수', '목', '금', '토'];
        weekdays.forEach(day => grid.innerHTML += `<div class="calendar-header">${day}</div>`);

        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        for (let i = 0; i < firstDayOfMonth; i++) grid.appendChild(document.createElement('div'));

        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dayEl = document.createElement('div');
            dayEl.className = 'day';

            if (date >= startDate && date <= endDate) {
                dayEl.dataset.date = toYYYYMMDD(date);
                if (date.getDay() === 0 || date.getDay() === 6) dayEl.classList.add('weekend');
                const status = attendanceData[dayEl.dataset.date];
                if (status) dayEl.classList.add(status);
            } else {
                dayEl.classList.add('not-in-range');
            }
            dayEl.innerHTML = `<div class="day-content">${day}</div>`;
            grid.appendChild(dayEl);
        }
        monthContainer.appendChild(grid);
        return monthContainer;
    }

    /** 날짜 클릭 -> 팝업 표시 */
    function handleDayClick(e) {
        const dayEl = e.target.closest('.day');
        if (!dayEl || dayEl.classList.contains('not-in-range') || dayEl.classList.contains('weekend')) {
            if (!e.target.closest('.day-popup')) hidePopup();
            return;
        }

        if (selectedDayElement) selectedDayElement.classList.remove('selected');
        selectedDayElement = dayEl;
        selectedDayElement.classList.add('selected');
        
        const date = selectedDayElement.dataset.date;
        dayPopup.dataset.date = date; // 팝업에 날짜 정보 저장

        // 팝업 위치 계산
        const calendarRect = calendarContainer.getBoundingClientRect();
        const dayRect = selectedDayElement.getBoundingClientRect();
        dayPopup.style.left = `${dayRect.left - calendarRect.left + dayRect.width + 5}px`;
        dayPopup.style.top = `${dayRect.top - calendarRect.top + calendarContainer.scrollTop}px`;
        dayPopup.style.display = 'block';

        // 팝업의 라디오 버튼 상태 업데이트
        const currentStatus = attendanceData[date];
        document.querySelectorAll('input[name="popup-status"]').forEach(r => r.checked = false);
        if (currentStatus) {
            document.querySelector(`input[name="popup-status"][value="${currentStatus}"]`).checked = true;
        }
    }

    /** 팝업 내 상태 변경 핸들러 */
    function handleStatusChange(e) {
        if (e.target.name !== 'popup-status') return;

        const newStatus = e.target.value;
        const date = dayPopup.dataset.date;
        const dayEl = document.querySelector(`.day[data-date="${date}"]`);
        if (!dayEl) return;

        const isAlreadySelected = attendanceData[date] === newStatus;

        if (isAlreadySelected) {
            delete attendanceData[date];
            e.target.checked = false;
            dayEl.classList.remove('present', 'absent', 'late', 'early', 'vacation');
        } else {
            if (newStatus === 'vacation') {
                const stats = calculateAllStats();
                if (stats.totalStats.vacation >= stats.availableVacation) {
                    alert('사용 가능한 휴가일수가 부족합니다.');
                    e.target.checked = false;
                    const oldStatus = attendanceData[date];
                    if (oldStatus) document.querySelector(`input[name="popup-status"][value="${oldStatus}"]`).checked = true;
                    return;
                }
            }
            attendanceData[date] = newStatus;
            dayEl.classList.remove('present', 'absent', 'late', 'early', 'vacation');
            dayEl.classList.add(newStatus);
        }
        updateStatsDisplay();
    }

    // --- 아래 통계 계산 로직은 이전과 동일 ---

    /** 모든 통계 계산 */
    function calculateAllStats() {
        if (!startDate) return null;
        
        const result = {
            totalStats: { totalWeekdays: 0, present: 0, absent: 0, late: 0, early: 0, vacation: 0, penaltyAbsent: 0, rate: 0 },
            periodStats: [],
            availableVacation: calculateAvailableVacation()
        };

        let periodStartDate = new Date(startDate);
        while (periodStartDate <= endDate) {
            let periodEndDate = new Date(periodStartDate);
            periodEndDate.setMonth(periodEndDate.getMonth() + 1);
            periodEndDate.setDate(periodEndDate.getDate() - 1);
            if (periodEndDate > endDate) periodEndDate = new Date(endDate);

            const periodData = { name: `${periodStartDate.getFullYear()}년 ${periodStartDate.getMonth() + 1}월 기준`, startDateStr: toYYYYMMDD(periodStartDate), endDateStr: toYYYYMMDD(periodEndDate), totalWeekdays: 0, present: 0, absent: 0, late: 0, early: 0, vacation: 0 };

            let currentDate = new Date(periodStartDate);
            while (currentDate <= periodEndDate) {
                if (currentDate.getDay() !== 0 && currentDate.getDay() !== 6) {
                    periodData.totalWeekdays++;
                    const status = attendanceData[toYYYYMMDD(currentDate)] || 'present';
                    if (periodData[status] !== undefined) periodData[status]++;
                }
                currentDate.setDate(currentDate.getDate() + 1);
            }
            
            const penalty = Math.floor((periodData.late + periodData.early) / 3);
            const attendanceDays = periodData.totalWeekdays - periodData.vacation;
            const effectiveAbsents = periodData.absent + penalty;
            periodData.rate = attendanceDays > 0 ? ((attendanceDays - effectiveAbsents) / attendanceDays) * 100 : 0;
            
            result.periodStats.push(periodData);

            Object.keys(result.totalStats).forEach(key => {
                if (key !== 'rate' && periodData[key] !== undefined) result.totalStats[key] += periodData[key];
            });
            
            periodStartDate.setMonth(periodStartDate.getMonth() + 1);
        }

        result.totalStats.penaltyAbsent = Math.floor((result.totalStats.late + result.totalStats.early) / 3);
        const totalAttDays = result.totalStats.totalWeekdays - result.totalStats.vacation;
        const totalEffAbsents = result.totalStats.absent + result.totalStats.penaltyAbsent;
        result.totalStats.rate = totalAttDays > 0 ? ((totalAttDays - totalEffAbsents) / totalAttDays) * 100 : 0;
        
        return result;
    }

    /** 통계 화면 업데이트 */
    function updateStatsDisplay() {
        const stats = calculateAllStats();
        if (!stats) return;

        document.getElementById('total-attendance-rate').textContent = `${stats.totalStats.rate.toFixed(2)}%`;
        document.getElementById('available-vacation').textContent = `${stats.availableVacation}일`;
        document.getElementById('total-days').textContent = `${stats.totalStats.totalWeekdays}일`;
        document.getElementById('present-days').textContent = `${stats.totalStats.present}일`;
        document.getElementById('absent-days').textContent = `${stats.totalStats.absent}일`;
        document.getElementById('late-days').textContent = `${stats.totalStats.late}회`;
        document.getElementById('early-days').textContent = `${stats.totalStats.early}회`;
        document.getElementById('vacation-days').textContent = `${stats.totalStats.vacation}일`;
        document.getElementById('penalty-absent').textContent = `${stats.totalStats.penaltyAbsent}일`;

        const periodContainer = document.getElementById('period-stats-container');
        periodContainer.innerHTML = '';
        stats.periodStats.forEach(p => {
            const item = document.createElement('div');
            item.className = 'period-stat-item';
            item.innerHTML = `
                <h4>${p.name}</h4>
                <p><strong>기간:</strong> ${p.startDateStr} ~ ${p.endDateStr}</p>
                <p><strong>출석률:</strong> <span style="color:${p.rate < 90 ? '#f44336' : '#4caf50'}; font-weight: bold;">${p.rate.toFixed(2)}%</span></p>
                <p>수업:${p.totalWeekdays}, 출석:${p.present}, 결석:${p.absent}, 지각/조퇴:${p.late}/${p.early}</p>
            `;
            periodContainer.appendChild(item);
        });
    }

    /** 사용 가능 휴가일수 계산 */
    function calculateAvailableVacation() {
        if (!startDate) return 0;
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        let periodCount = 0;
        let tempPeriodStart = new Date(startDate);
        while (true) {
            let nextPeriodStart = new Date(tempPeriodStart);
            nextPeriodStart.setMonth(nextPeriodStart.getMonth() + 1);
            if (today >= nextPeriodStart) {
                periodCount++;
                tempPeriodStart = nextPeriodStart;
            } else {
                break;
            }
        }
        return 1 + periodCount;
    }
    
    /** Date 객체를 YYYY-MM-DD 문자열로 변환 */
    function toYYYYMMDD(date) {
        return date.toISOString().split('T')[0];
    }
});