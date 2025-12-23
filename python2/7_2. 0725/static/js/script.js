// Get the modal
var addModal = document.getElementById("addModal");
var updateModal = document.getElementById("updateModal");

// Get the button that opens the modal
var addBtn = document.getElementById("addBtn");
var updateBtns = document.querySelectorAll(".updateBtn");

// Get the <span> element that closes the modal
var closeAddBtn = document.getElementById("closeAddBtn");
var closeUpdateBtn = document.getElementById("closeUpdateBtn");

// When the user clicks the button, open the modal
addBtn.onclick = function() {
    addModal.style.display = "block";
}

// When the user clicks on update button, open the update modal
updateBtns.forEach(function(btn) {
    btn.onclick = function() {
        var customerId = this.dataset.customerId;
        // Fetch customer data and populate the form
        var customer = Array.from(document.querySelectorAll('table tbody tr')).find(tr => tr.querySelector('td:first-child').textContent === customerId);
        var name = customer.querySelector('td:nth-child(2)').textContent;
        var age = customer.querySelector('td:nth-child(3)').textContent;
        var gender = customer.querySelector('td:nth-child(4)').textContent;
        var purchaseAmount = customer.querySelector('td:nth-child(5)').textContent.replace(/[^0-9]/g, ''); // '원' 및 쉼표 제거
        var purchaseDate = customer.querySelector('td:nth-child(6)').textContent;

        document.getElementById('update_customer_id').value = customerId;
        document.getElementById('update_name').value = name;
        document.getElementById('update_age').value = age;
        document.getElementById('update_gender').value = gender;
        document.getElementById('update_purchase_amount').value = purchaseAmount;
        document.getElementById('update_purchase_date').value = purchaseDate;

        updateModal.style.display = "block";
    }
});

// 모달 닫기 함수 추가
function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

// 기존 닫기 버튼 이벤트를 closeModal 함수 사용하도록 수정
closeAddBtn.onclick = function() {
    closeModal('addModal');
}

closeUpdateBtn.onclick = function() {
    closeModal('updateModal');
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        closeModal(event.target.id);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // 1. 백엔드 API로부터 차트 데이터를 비동기적으로 가져옵니다.
    fetch('/api/chart/gender')
        .then(response => response.json()) // 응답을 JSON으로 파싱합니다.
        .then(data => {
            // 2. Chart.js를 사용하여 차트를 생성합니다.
            const ctx = document.getElementById('genderChart').getContext('2d');
            
            new Chart(ctx, {
                type: 'bar', // 차트 종류: 막대 차트
                data: {
                    labels: data.labels, // x축 레이블 (예: ['Female', 'Male'])
                    datasets: [{
                        label: '총 구매금액',
                        data: data.values, // 실제 데이터 (예: [550000, 800000])
                        backgroundColor: [ // 막대 색상
                            'rgba(255, 99, 132, 0.5)',
                            'rgba(54, 162, 235, 0.5)'
                        ],
                        borderColor: [ // 막대 테두리 색상
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true // y축을 0부터 시작
                        }
                    }
                }
            });
        })
        .catch(error => console.error('차트 데이터 로딩 실패:', error)); // 에러 발생 시 콘솔에 로그 출력
});
