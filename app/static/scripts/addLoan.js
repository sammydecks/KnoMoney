document.getElementById("addLoan").addEventListener("click", function () {
    const loanContainer = document.getElementById("loanContainer");
    const loanCount = loanContainer.getElementsByClassName("loanEntry").length + 1;

    const newLoan = document.createElement("fieldset");
    newLoan.classList.add("loanEntry", "border", "p-2", "mb-3");

    newLoan.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <legend class="lead text-center">Loan ${loanCount}</legend>
            <button type="button" class="btn-close" aria-label="Close"></button>
        </div>
        <div class="row">
            <div class="col-12 col-md">
                <label for="semester" class="form-label">Semester Loan was Taken:</label>
                <select name="semester[]" class="semester form-select" required>
                    <option value="" disabled selected>-- select --</option>
                </select>
            </div>
            <div class="col-12 col-md">
                <label for="type" class="form-label">Loan Type:</label>
                <select name="type[]" class="form-select" required>
                    <option value="" disabled selected>-- select --</option>
                    <option value="unsubsidized">Unsubsidized</option>
                    <option value="subsidized">Subsidized</option>
                </select>
            </div>
            <div class="col-12 col-md">
                <label for="balance" class="form-label">Balance ($): </label>
                <input type="number" class="form-control" name="balance[]" placeholder="Loan Balance" min="0.01" max="100000" step="0.01" required>
            </div>
            <div class="col-12 col-md">
                <label for="interest" class="form-label">Interest Rate (%): </label>
                <input type="number" class="form-control" name="interest[]" placeholder="Loan Interest Rate" min="0.01" max="99.99" step="0.01" required>
            </div>
        </div>
    `;

    loanContainer.appendChild(newLoan);

    // Populate the semester dropdown for the new loan
    populateSemesterDropdowns();

    // Add event listener to remove the loan entry when "X" is clicked
    newLoan.querySelector(".btn-close").addEventListener("click", function () {
        loanContainer.removeChild(newLoan);
    });
});