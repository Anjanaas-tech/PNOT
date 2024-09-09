// Function to validate login form
function validateLoginForm() {
    const username = document.getElementById('id_username').value.trim();
    const password = document.getElementById('id_password').value.trim();
    const errorElement = document.getElementById('form-error');

    if (username === '' || password === '') {
        errorElement.textContent = 'Both fields are required.';
        return false;
    }

    errorElement.textContent = ''; // Clear previous error
    return true;
}

// Add event listener to the login form
document.addEventListener('DOMContentLoaded', function() {
    // Add simple fade-in effect
    const loginContainer = document.querySelector('.login-container');
    if (loginContainer) {
        loginContainer.style.opacity = 0;
        setTimeout(() => loginContainer.style.opacity = 1, 500);
    }

    // Example of a dynamic update
    const toggleButton = document.getElementById('toggle-button');
    const infoBox = document.getElementById('info-box');

    if (toggleButton && infoBox) {
        toggleButton.addEventListener('click', function() {
            infoBox.classList.toggle('hidden'); // Toggle visibility
        });
    }
});
