/* 
Calculate.js
This file calculates the loan and returns the total saved interest amount

*/

// import * as namespace from "../calculation.py";


document.getElementById("calculate").addEventListener("click", async function() {
    const resultsContainer = document.getElementById("resultContainer");

    // save graduation date from input field
    const gradDate = document.getElementById("graduation").value;

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
            interest: parseFloat(interest),
            type: type,
            dateReceived: received
        })
    });

    
    //Call Python function with API request
    try {
        // frontend calls server endpoint with url calculate_interest
        const response = await fetch("/calculate_interest", {
            //HTTP request settings to send data to the backend as JSON
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({gradDate, loans}) //converts JSON object to JSON string
        });

        //if there is an error with request, throw error
        if (!response.ok) throw new Error("Failed to fetch interest calculation");
        
        // parses response body as JSON
        // FUTURE IMPLEMENTATION: This will also send in totalSaved and possibly recommendations in the future 
        const data = await response.json();

        //extracts value in totalInterest key
        const totalInterest = data.totalInterest;

        // Add the results underneath on the same page
        const results = document.createElement("fieldset");
        // results.innerText = "RESULTS";
        results.innerHTML = `
            <div class="border border-dark p-3 mt-3 text-center">
                <h2 class="mb-3">RESULTS</h2>
                <p class="fw-bold">Total Accrued Interest by Graduation Date:</p>
                <p class="mb-2">${totalInterest}</p>
                <p class="fw-bold">Potential Savings (Over 10 Years):</p>
                <p>In Da Works</p>
            </div>
        `;

        // Add HTML content to the page
        resultsContainer.appendChild(results);

        // Scroll to results section
        results.scrollIntoView({behavior: "smooth"});

    }
    catch (error) {
        console.error("Error in Calculating Interest:", error);
    }
});