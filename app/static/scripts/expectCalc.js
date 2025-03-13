/* 
expectCalc.js
This file connects to the basic calculation that users can do on the homepage
*/


// Function to get CSRF token from cookies
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

document.getElementById("expectedDebt").addEventListener("submit", async function (event) {
    event.preventDefault();

    // Get the debt range selected
    let selectedDebtRange = event.submitter?.value;
    console.log("Selected Debt Range:", selectedDebtRange);
    // Get the graduation date
    const gradDate = document.getElementById("graduationDate").value;

    try {
        // Fetch CSRF token and include in request
        const csrfToken = getCSRFToken();
        // call server endpoint with url calculate_savings_simple
        const response = await fetch("/calculate_savings_simple", {
            //HTTP request to send data to backend
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({gradDate, selectedDebtRange})
        });
        if (!response.ok) throw new Error("Failed to fetch potential savings calculation");

        // parse response body as JSON and take totalSaved value
        const data = await response.json();
        //extracts value in data key
        const totalSaved = data.totalSaved;

        // Fill in data on Home Page
        let savingsAmt = document.getElementById("savingsAmt");
        savingsAmt.innerHTML = totalSaved;
        document.querySelector("#saveContainer").classList.remove("d-none");
    }
    catch (error) {
        console.error("Error in Calculating Potential Savings:", error);
    }
});

document.addEventListener("DOMContentLoaded", function () {
    // Initialize all popovers on the page
    var popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    var popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
  });

