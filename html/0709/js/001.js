const sensorData = [
    { "time": "08:00", "temperature": 22, "humidity": 45, "vibration": 0.5 },
    { "time": "09:00", "temperature": 24, "humidity": 50, "vibration": 0.7 },
    { "time": "10:00", "temperature": 23, "humidity": 48, "vibration": 0.6 },
    { "time": "11:00", "temperature": 25, "humidity": 55, "vibration": 0.8 },
    { "time": "12:00", "temperature": 26, "humidity": 52, "vibration": 0.9 },
    { "time": "13:00", "temperature": 27, "humidity": 54, "vibration": 1.0 },
    { "time": "14:00", "temperature": 28, "humidity": 56, "vibration": 1.2 },
    { "time": "15:00", "temperature": 29, "humidity": 58, "vibration": 1.1 },
    { "time": "16:00", "temperature": 28, "humidity": 60, "vibration": 1.0 },
    { "time": "17:00", "temperature": 27, "humidity": 59, "vibration": 0.9 },
    { "time": "18:00", "temperature": 25, "humidity": 57, "vibration": 0.8 },
    { "time": "19:00", "temperature": 24, "humidity": 55, "vibration": 0.7 },
    { "time": "20:00", "temperature": 23, "humidity": 53, "vibration": 0.6 },
    { "time": "21:00", "temperature": 22, "humidity": 50, "vibration": 0.5 },
    { "time": "22:00", "temperature": 21, "humidity": 48, "vibration": 0.4 }
];

document.querySelector("#thead").innerHTML =
    `<tr>
        <th>시간</th>
        <th>온도(ºC)</th>
        <th>습도(%)</th>
        <th>진동(m/s²)</th>
    </tr>`;

let sensorString = '';

sensorData.forEach((data) => {
    sensorString +=
        `<tr>
            <td>${data["time"]}</td>
            <td>${data["temperature"]}</td>
            <td>${data["humidity"]}</td>
            <td>${data["vibration"]}</td>
        </tr>`;
});

document.querySelector("#tbody").innerHTML = sensorString;

// 예제 그래프 그리기
const ctx = document.getElementById('myChart');
const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
        }]
    },
    options: {
        scales: {
        y: {
            beginAtZero: true
        }
        }
    }
});

// 내 데이터로 라인형 그래프 그리기
const ctx2 = document.getElementById('myChart2').getContext('2d');
const chart2 = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: sensorData.map(data => data.time),
        datasets: [
            {
                label: '온도 (°C)',
                data: sensorData.map(data => data.temperature),
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false,
            },
            {
                label: '습도 (%)',
                data: sensorData.map(data => data.humidity),
                borderColor: 'rgba(54, 162, 235, 1)',
                fill: false,
            },
            {
                label: '진동 (m/s²)',
                data: sensorData.map(data => data.vibration),
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
            },
        ]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: '시간'
                }
            },
            y: {
                title: {
                    display: true,
                    text: '값'
                }
            }
        }
    }
});

// 바형 그래프
const ctx3 = document.getElementById('myChart3').getContext('2d');
const chart3 = new Chart(ctx3, {
    type: 'bar',
    data: {
        labels: sensorData.map(data => data.time),
        datasets: [
            {
                label: '온도 (°C)',
                data: sensorData.map(data => data.temperature),
                backgroundColor: 'rgba(255, 99, 132, 1)',
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false,
            },
            {
                label: '습도 (%)',
                data: sensorData.map(data => data.humidity),
                backgroundColor: 'rgba(54, 162, 235, 1)',
                borderColor: 'rgba(54, 162, 235, 1)',
                fill: false,
            },
            {
                label: '진동 (m/s²)',
                data: sensorData.map(data => data.vibration),
                backgroundColor: 'rgba(75, 192, 192, 1)',
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
            },
        ]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: '시간'
                }
            },
            y: {
                title: {
                    display: true,
                    text: '값'
                }
            }
        }
    }
});

// 원형 그래프1
const ctx4 = document.getElementById('myChart4').getContext('2d');
const chart4 = new Chart(ctx4, {
    type: 'doughnut',
    data: {
        labels: sensorData.map(data => data.time),
        datasets: [
            {
                data: sensorData.map(data => data.temperature),
                backgroundColor: 'rgba(255, 99, 132, 1)',
                hoverOffset: 4,
            }
        ]
    }
});

// 원형 그래프2
const ctx5 = document.getElementById('myChart5').getContext('2d');
const chart5 = new Chart(ctx5, {
    type: 'doughnut',
    data: {
        labels: sensorData.map(data => data.time),
        datasets: [
            {
                data: sensorData.map(data => data.humidity),
                backgroundColor: 'rgba(54, 162, 235, 1)',
                hoverOffset: 4,
            }
        ]
    }
});

// 원형 그래프3
const ctx6 = document.getElementById('myChart6').getContext('2d');
const chart6 = new Chart(ctx6, {
    type: 'doughnut',
    data: {
        labels: sensorData.map(data => data.time),
        datasets: [
            {
                data: sensorData.map(data => data.vibration),
                backgroundColor: 'rgba(75, 192, 192, 1)',
                hoverOffset: 4,
            }
        ]
    }
});