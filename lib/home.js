document.addEventListener('DOMContentLoaded', function() {
    const screens = document.querySelectorAll('.screen');
    
    function showScreen(screenId) {
        screens.forEach(screen => {
            screen.classList.add('hidden');
        });
        document.getElementById(screenId).classList.remove('hidden');
    }

    window.showScreen = showScreen;

    window.signup = function(event) {
        event.preventDefault();
        // Perform signup logic here
        // For now, simply show the signup complete screen
        showScreen('signup_complete_screen');
    }

    window.login = function(event) {
        event.preventDefault();
        // Perform login logic here
        // For now, simply show the waiting screen
        showScreen('waiting_screen');
    }

    window.checkReservation = function(event) {
        event.preventDefault();
        // Perform reservation check logic here
    }

    window.completePayment = function() {
        // Perform payment completion logic here
        showScreen('payment_complete_screen');
    }

    showScreen('waiting_screen'); // Initialize with the waiting screen
});
