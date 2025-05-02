// Mount Table Web Application JavaScript

// Form validation for signup form
function validateSignupForm() {
    const form = document.getElementById("signupForm");
    if (!form) return;

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        // Validate password match
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        // Check email is mount email
        const email = document.getElementById("email").value;
        if (!email.endsWith("@msmary.edu") && !email.endsWith("@email.msmary.edu")) {
            alert("Please use your Mount St. Mary's University email address.");
            return;
        }

        // If validation passes, submit the form
        let id = "0000001";
        alert(`Account created successfully! Your ID number is: ${id}`);
        
        // Redirect test
        window.location.href = "login.html";
        // In production, submit to server
        // form.submit();
    });
}

// Form validation for food request form
function validateFoodRequestForm() {
    const form = document.getElementById("foodRequestForm");
    if (!form) return;

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        // Get all selected items
        const selectedItems = Array.from(document.querySelectorAll('input[name="items"]:checked'))
            .map(input => input.value);

        if (selectedItems.length === 0) {
            alert("Please select at least one item.");
            return;
        }

        // Note to self, possibly make a page between confirmation, to show 'cart'
        alert("Your request has been submitted successfully! You can pick up your items from the Mount Table tomorrow.");

        // redirect to a confirmation page
        // window.location.href = "confirmation.html";
    });
}

// Form validation for login form
function validateLoginForm() {
    const form = document.getElementById("loginForm");
    if (!form) return;

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const studentId = document.getElementById("studentId").value;
        const password = document.getElementById("password").value;

        if (!studentId || !password) {
            alert("Please enter both your Student ID and Password.");
            return;
        }

        // Auto accept anything right now
        alert("Login successful!");

        // Redirect test
        window.location.href = "orderForm.html";
    });
}

// Forgot ID form validation
function validateForgotIdForm() {
    const form = document.getElementById("forgotIdForm");
    if (!form) return;

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const firstName = document.getElementById("firstName").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if (!firstName || !email || !password) {
            alert("Please fill in all fields.");
            return;
        }

        // In production, this would verify with the server
        alert("Verification successful! Your Student ID is: MT12345");

        // Redirect to login page
        // window.location.href = "login.html";
    });
}

// Toggle mobile navigation menu
function setupMobileNav() {
    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.getElementById("navMenu");

    if (!menuToggle || !navMenu) return;

    menuToggle.addEventListener("click", function() {
        navMenu.classList.toggle("show");
    });
}

// Automatically initialize all scripts when DOM is ready
document.addEventListener("DOMContentLoaded", function() {
    validateSignupForm();
    validateFoodRequestForm();
    validateLoginForm();
    validateForgotIdForm();
    setupMobileNav();
});
