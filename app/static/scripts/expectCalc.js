document.getElementById("expectedDebt").addEventListener("submit", function (event) {
    event.preventDefault();
    // Get the debt range selected
    let selectedDebtRange = event.submitter?.value;
        
    // Get the graduation date
    const gradDate = document.getElementById("graduationDate").value;

    let savingsAmt = document.getElementById("savingsAmt");
    // MIMI: here is fill in for savings amount calculation
    savingsAmt.innerHTML = selectedDebtRange;
    document.querySelector("#saveContainer").classList.remove("d-none");
});

document.addEventListener("DOMContentLoaded", function () {
    // Initialize all popovers on the page
    var popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    var popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
  });

