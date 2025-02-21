document.getElementById("addLoan").addEventListener("click", function() {
    const loanContainer = document.getElementById("loanContainer");
    const loanCount = loanContainer.getElementsByClassName("loanEntry").length + 1;

    const newLoan = document.createElement("fieldset");
    newLoan.classList.add("loanEntry");
    newLoan.innerHTML = `
        <legend>Loan ${loanCount}</legend>
        <label for="balance">Balance ($): </label>
        <input type="number" name="balance[]" min="0.01" step="0.01" required>
        <label for="interest">Interest Rate (%): </label>
        <input type="number" name="interest[]" min="0.01" max="99.99" step="0.01" required>
        <label for="type">Loan Type:</label>
        <select name="type[]" required>
            <option value="" disabled selected>-- Select --</option>
            <option value="unsubsidized">Unsubsidized</option>
            <option value="subsidized">Subsidized</option>
        </select>
        <label for="received">Date Received:</label>
        <input type="date" name="received[]" required>
    `;

    loanContainer.appendChild(newLoan);
});