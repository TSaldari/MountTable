// Mount Table Web Application JavaScript

// Form validation for signup form
function validateSignupForm() {
    const form = document.getElementById("signupForm");
    if (!form) return;

    form.addEventListener("submit", function (event) {

        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;
        const email = document.getElementById("email").value;

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        if (!email.endsWith("@msmary.edu") && !email.endsWith("@email.msmary.edu")) {
            alert("Please use your Mount St. Mary's University email address.");
            return;
        }

        // For demo purposes only, remove server-side ID handling
        alert("Form is valid! Server will create your account and ID.");

        // Optionally submit to server if you have a Flask route
        form.submit();
    });
}


// Form validation for food request form
function validateFoodRequestForm() {
    const form = document.getElementById("foodRequestForm");
    if (!form) return;

    form.addEventListener("submit", function (event) {

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

    form.addEventListener("submit", function (event) {
        const studentId = document.getElementById("studentId").value;
        const password = document.getElementById("password").value;

        if (!studentId || !password) {
            event.preventDefault();
            alert("Please enter both your Student ID and Password.");
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {

    // Selects all food item check boxes
    const itemCheckboxes = document.querySelectorAll('#foodRequestForm input[name="items"]');
    // Selects all dietary restriction check boxes
    const restrictionCheckboxes = document.querySelectorAll('input[name="dietaryRestrictions"]');

    // Disables an item utilizing CSS class 
    function disableFoodItem(itemElement, reason) {
        const foodItemDiv = itemElement.closest('.food-item');
        if (foodItemDiv) {
            foodItemDiv.classList.add('disabled'); // adds CSS class
            foodItemDiv.setAttribute('data-reason', reason); // Sets the reason for disable
            itemElement.disabled = true; // Disables checkbox
        }
    }

    // Enables an item
    function enableFoodItem(itemElement) {
        const foodItemDiv = itemElement.closest('.food-item');
        if (foodItemDiv) {
            // Only re-enable if not out-of-stock
            const itemValue = itemElement.value;
            const isOutOfStock = inventory.hasOwnProperty(itemValue) && inventory[itemValue] <= 0;

            if (!isOutOfStock) {
                foodItemDiv.classList.remove('disabled'); // Removes CSS class
                foodItemDiv.removeAttribute('data-reason'); // Removes attribute
                itemElement.disabled = false;
            } else {
                // Ensure out-of-stock items still show the correct reason
                foodItemDiv.setAttribute('data-reason', 'Out of Stock');
            }
        }
    }

    // Handling allergies
    function handleAllergyCheck() {
        // Get all currently active restrictions
        const activeRestrictions = Array.from(restrictionCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);

        // Iterate through all food items
        itemCheckboxes.forEach(checkbox => {
            const itemValue = checkbox.value;
            const itemAllergens = ALLERGEN_MAP[itemValue] || []; // Get allergens for this item

            let conflict = false;
            let conflictReason = 'Allergy';

            // Check for conflict with any active restriction
            if (activeRestrictions.length > 0) {
                for (const restriction of activeRestrictions) {
                    if (itemAllergens.includes(restriction)) {
                        conflict = true;
                        // Set the specific reason for better feedback
                        conflictReason = `Contains ${restriction.charAt(0).toUpperCase() + restriction.slice(1)}`;
                        break;
                    }
                }
            }

            // Apply or remove the disabled state
            if (conflict) {
                disableFoodItem(checkbox, conflictReason);
            } else {
                enableFoodItem(checkbox);
            }
        });
    }

    // Event Listeners
    // Attaches the check function to every restriction checkbox change
    restrictionCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', handleAllergyCheck);
    });

    // Initial inventory check 
    itemCheckboxes.forEach(checkbox => {
        const itemValue = checkbox.value;
        if (inventory.hasOwnProperty(itemValue)) {
            const currentQuantity = inventory[itemValue];
            if (currentQuantity !== undefined && currentQuantity <= 0) {
                disableFoodItem(checkbox, 'Out of Stock');
            }
        }
    });

    // Run the allergy check once when the page loads
    handleAllergyCheck();
});

// Forgot ID form validation -- was removed, may add back later
function validateForgotIdForm() {
    const form = document.getElementById("forgotIdForm");
    if (!form) return;

    form.addEventListener("submit", function (event) {
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

    menuToggle.addEventListener("click", function () {
        navMenu.classList.toggle("show");
    });
}

// Automatically initialize all scripts when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
    validateSignupForm();
    validateFoodRequestForm();
    validateLoginForm();
    validateForgotIdForm();
    setupMobileNav();
});

// Inventory Management - Stock Adjustment Functionality
document.addEventListener('DOMContentLoaded', function () {
    // Handle increase button clicks
    const increaseButtons = document.querySelectorAll('.increase-btn');
    increaseButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const itemId = this.getAttribute('data-item-id');
            const adjustInput = document.getElementById('adjust-' + itemId);
            const amount = parseInt(adjustInput.value) || 1;

            // Set the hidden input value
            document.getElementById('amount-increase-' + itemId).value = amount;

            // Submit the form
            document.getElementById('form-increase-' + itemId).submit();
        });
    });

    // Handle decrease button clicks
    const decreaseButtons = document.querySelectorAll('.decrease-btn');
    decreaseButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const itemId = this.getAttribute('data-item-id');
            const currentStock = parseInt(this.getAttribute('data-current-stock'));
            const adjustInput = document.getElementById('adjust-' + itemId);
            const amount = parseInt(adjustInput.value) || 1;

            // Check if decrease would result in negative stock
            if (amount > currentStock) {
                alert('Cannot decrease by ' + amount + '. Current stock is only ' + currentStock + '.');
                return;
            }

            // Set the hidden input value
            document.getElementById('amount-decrease-' + itemId).value = amount;

            // Submit the form
            document.getElementById('form-decrease-' + itemId).submit();
        });
    });
});