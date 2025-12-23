const popup = document.getElementById('popup');
const overlay = document.getElementById('overlay');

document.getElementById('openPopup').addEventListener('click', function() {
    popup.style.display = 'block';
    overlay.style.display = 'block';
});

overlay.addEventListener('click', function() {
    popup.style.display = 'none';
    overlay.style.display = 'none';
});