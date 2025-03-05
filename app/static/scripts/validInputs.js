document.addEventListener("DOMContentLoaded", function () {
    const graduationDateInput = document.getElementById("graduationDate");
    const form = document.getElementById("loanForm");

    function validateLoanDates() {
        const graduationDate = new Date(graduationDateInput.value);
        const loanDateInputs = document.querySelectorAll('input[name="received[]"]');

        loanDateInputs.forEach(input => {
            const loanDate = new Date(input.value);
            if (loanDate >= graduationDate) {
                input.setCustomValidity("Loan date must be before graduation date.");
            } else {
                input.setCustomValidity("");
            }
        });
    }

    // Validate loan dates whenever the graduation date changes
    graduationDateInput.addEventListener("change", validateLoanDates);

    // Validate loan dates when loan dates change
    document.getElementById("loanContainer").addEventListener("input", function (event) {
        if (event.target.name === "received[]") {
            validateLoanDates();
        }
    });

    // Final check before submission
    form.addEventListener("submit", function (event) {
        validateLoanDates();
        if (!form.checkValidity()) {
            event.preventDefault(); // Prevent form submission if invalid
        }
    });
});