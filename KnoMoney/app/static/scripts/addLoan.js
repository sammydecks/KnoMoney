document.getElementById("addLoan").addEventListener("click", function() {
    const loanContainer = document.getElementById("loanContainer");
    const loanCount = loanContainer.getElementsByClassName("loanEntry").length + 1;

    const newLoan = document.createElement("fieldset");
    newLoan.classList.add("loanEntry");
    newLoan.innerHTML = `
        <legend>Loan ${loanCount}</legend>
        <label for="balance">Balance ($): </label>
        <input type="number" name="balance[]" min="1">
        <label for="interest">Interest Rate (%): </label>
        <input type="number" name="interest[]" min="1">
        <label for="type">Loan Type:</label>
        <select name="type[]">
            <option value="" disabled selected>-- Select --</option>
            <option value="unsubsidized">Unsubsidized</option>
            <option value="subsidized">Subsidized</option>
        </select>
        <label for="received">Date Received:</label>
        <input type="date" name="received[]">
    `;

    loanContainer.appendChild(newLoan);
});