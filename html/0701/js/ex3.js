function calculateDiscount(){
    let membershipLevel = document.getElementById("membershipLevel").value;

    if(membershipLevel === 'gold'){
        document.getElementById("discountResult").textContent = `${membershipLevel}등급은 할인율 20% 입니다`;
    }else if(membershipLevel === 'silver'){
        document.getElementById("discountResult").textContent = `${membershipLevel}등급은 할인율 10% 입니다`;
    }else if(membershipLevel === '1234'){
        location.href = "https://naver.com";
    }else{
        document.getElementById("discountResult").textContent = "잘못 입력하셨습니다";
    }
}