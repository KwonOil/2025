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
