/* 
Calculate.js
This file calculates the loan and returns the total saved interest amount

*/

// import * as namespace from "../calculation.py";

// Function to get CSRF token from cookies
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

document.getElementById("loanForm").addEventListener("submit", async function(event) {
    event.preventDefault();  // Prevent default form submission
    const resultsContainer = document.getElementById("resultContainer");

    // save graduation date from input field
    const gradDate = document.getElementById("graduationDate").value;

    // save each loan information into an array
    loans = [] 
    // select all fieldsets in loan container and loop through each loan
    document.querySelectorAll(".loanEntry").forEach((loanEntry, index) => {
        const balance = loanEntry.querySelector('input[name="balance[]"]').value;
        const interest = loanEntry.querySelector('input[name="interest[]"]').value;
        const type = loanEntry.querySelector('select[name="type[]"]').value;
        const received = loanEntry.querySelector('input[name="received[]"]').value;
 
        // create JSON object and add to loans
        loans.push({
            loanNum: index + 1,
            principal: parseFloat(balance),
            interest: parseFloat(interest) / 100,
            type: type,
            dateReceived: received
        })
    });

    
    //Call Python function with API request
    try {
        // Fetch CSRF token and include in request
        const csrfToken = getCSRFToken();
        // frontend calls server endpoint with url calculate_interest
        const response = await fetch("/calculate_interest", {
            //HTTP request settings to send data to the backend as JSON
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken  // Include CSRF token in request headers
            },
            body: JSON.stringify({gradDate, loans}) //converts JSON object to JSON string
        });

        //if there is an error with request, throw error
        if (!response.ok) throw new Error("Failed to fetch interest calculation");
        
        // parses response body as JSON
        // FUTURE IMPLEMENTATION: This will also send in totalSaved and possibly recommendations in the future 
        const data = await response.json();

        //extracts value in totalInterest key
        const totalInterest = data.totalInterest;
        const totalSaved = data.totalSaved;
        const monthlyPay = data.monthlyPay;
        const savedGracePeriod = data.savedGracePeriod;
        const savedAllYears = data.savedAllYears;

        // Location to fill in totalInterest value
        let totalInterestField = document.getElementById("totalInterest");
        totalInterestField.innerHTML = totalInterest;
        let totalSavedField = document.getElementById("potentialSavings");
        totalSavedField.innerHTML = totalSaved;
        let monthlyPayField = document.getElementById("monthlyPayment");
        monthlyPayField.innerHTML = monthlyPay;
        let savedGracePeriodField = document.getElementById("whatIfPaid");
        savedGracePeriodField.innerHTML = savedGracePeriod;
        let savedAllYearsField = document.getElementById("whatIfSaved");
        savedAllYearsField.innerHTML = savedAllYears;

        // Make results and recommendations containers visible
        document.querySelector("#resultContainer .d-none")?.classList.remove("d-none");
        document.querySelector("#recommendationsContainer .d-none")?.classList.remove("d-none");

        // Scroll to the results section every time
        setTimeout(() => {
            resultsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 100);

    }
    catch (error) {
        console.error("Error in Calculating Interest:", error);
    }
});