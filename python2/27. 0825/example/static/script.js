document.addEventListener('DOMContentLoaded', function() {
    const colorButton = document.getElementById('colorButton');
    const greetButton = document.getElementById('greetButton');
    const message = document.getElementById('message');
    const container = document.querySelector('.container');

    // Color change button functionality
    colorButton.addEventListener('click', function() {
        container.classList.toggle('color-changed');
    });

    // Greeting button functionality
    greetButton.addEventListener('click', function() {
        const greetings = [
            'Hello!',
            'Welcome to Flask!',
            'Static files are working!',
            'Have a great day!'
        ];
        const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];
        message.textContent = randomGreeting;

        // Add animation effect
        message.style.opacity = '0';
        message.style.transform = 'translateY(20px)';

        setTimeout(() => {
            message.style.transition = 'all 0.5s ease';
            message.style.opacity = '1';
            message.style.transform = 'translateY(0)';
        }, 100);
    });
});