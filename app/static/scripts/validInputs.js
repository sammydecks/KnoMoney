document.addEventListener("DOMContentLoaded", function () {
    // simple calc validation
    const graduationDateInput = document.getElementById("graduationDate");

    // Get today's date and format it as YYYY-MM 
    let today = new Date();
    let minMonth = today.toISOString().slice(0, 7); // Extract YYYY-MM format

    graduationDateInput.setAttribute("min", minMonth); // Set min to current or future months

    // old calculator validation
    const graduationDateInput2 = document.getElementById("graduationDate2");
    const form = document.getElementById("loanForm");

    today = new Date().toISOString().split("T")[0]; 
    graduationDateInput2.setAttribute("min", today); // only today or future grad dates

    function validateLoanDates() {
        const graduationDate = new Date(graduationDateInput2.value);
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
    graduationDateInput2.addEventListener("change", validateLoanDates);

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