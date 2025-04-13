/* 
calculate.js
This file calculates the loan and returns the total saved interest amount

*/

// import * as namespace from "../calculation.py";

// Function to get CSRF token from cookies
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

// displaying results based on unsubsidized vs subsidized
function toggleResults(showId, hideId) {
    document.querySelector(`#${showId} fieldset > div`).classList.remove("d-none");
    document.querySelector(`#${hideId} fieldset > div`).classList.add("d-none");
}

// listener for inputting corresponding interest rate for semester
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("loanContainer").addEventListener("change", async function(event) {
        if (!event.target.classList.contains("semester")) { return; }
        const loanEntry = event.target.closest(".loanEntry");  // Find closest loan entry
        if (!loanEntry) return;

        // select semester for given loan
        const semester = event.target.value;

        // error is semester is not filled?
        if (!semester) {
            console.warn("Missing semester.");
            return;
        }

        //Call Python function with API request
        try {
            // Fetch CSRF token and include in request
            const csrfToken = getCSRFToken();
            // frontend calls server endpoint with url calculate_interest
            const response = await fetch("/get_interestrate", {
                //HTTP request settings to send data to the backend as JSON
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken  // Include CSRF token in request headers
                },
                body: JSON.stringify({semester}) //converts JSON object to JSON string
            });

            //if there is an error with request, throw error
            if (!response.ok) throw new Error("Failed to fetch populate interest rate function");
            
            // parses response body as JSON
            const data = await response.json();

            const interest = data.interest;
            // Location to fill in totalInterest value
            let currentInterestField = loanEntry.querySelector("input[name='interest[]']");
            if (currentInterestField) {currentInterestField.value = interest;}
        }
        catch (error) {
            console.error("Error in Fetching Interest Rate:", error);
        }
    });
});

// CALCULATOR SUBMIT
// listener for calculate submit button
document.getElementById("loanForm").addEventListener("submit", async function(event) {
    event.preventDefault();  // Prevent default form submission
    let resultsContainer;

    // save graduation date from input field
    const gradDate = document.getElementById("graduationDate2").value;

    // save each loan information into an array
    loans = [] 
    // track unsubsidized vs subsidized loans
    let hasUnsub = false;
    // select all fieldsets in loan container and loop through each loan
    document.querySelectorAll(".loanEntry").forEach((loanEntry, index) => {
        const balance = loanEntry.querySelector('input[name="balance[]"]').value;
        const interest = loanEntry.querySelector('input[name="interest[]"]').value;
        const type = loanEntry.querySelector('select[name="type[]"]').value;
        const received = loanEntry.querySelector('select[name="semester[]"]').value;

        // found unsub loan, show corresponding result
        if (type === "unsubsidized") {
            hasUnsub = true;
        }

        // create JSON object and add to loans
        loans.push({
            loanNum: index + 1,
            principal: parseFloat(balance),
            interest: parseFloat(interest),
            type: type,
            semReceived: received
        })
    });

    //Call Python function with API request
    try {
        // Fetch CSRF token and include in request
        const csrfToken = getCSRFToken();

        // Calculate the sum of all loans (for both sub and unsub types)
        let response = await fetch("/calculate_sum_loans", {
            //HTTP request settings to send data to the backend as JSON
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken  // Include CSRF token in request headers
            },
            body: JSON.stringify({loans}) //converts JSON object to JSON string
        });
        const data = await response.json();
        let totalLoans = data.total;
       
        
        // calculate "What If" information
        let customPayment = document.getElementById("customPayment").value;
        response = await fetch("/calculate_whatif", {
            //HTTP request settings to send data to the backend as JSON
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken  // Include CSRF token in request headers
            },
            body: JSON.stringify({gradDate, loans, customPayment}) //converts JSON object to JSON string
        });
        const data2 = await response.json();
        //extracts value in returned dictionary
        const savedGracePeriod = data2.savedGracePeriod;
        const savedAllYears = data2.savedAllYears;


        const subResultsContent = document.querySelector("#subResultsContainer fieldset > div");
        const unsubResultsContent = document.querySelector("#unsubResultsContainer fieldset > div");

        if (hasUnsub) {
            response = await fetch("/calculate_sum_cap_loans", {
                //HTTP request settings to send data to the backend as JSON
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken  // Include CSRF token in request headers
                },
                body: JSON.stringify({gradDate, loans}) //converts JSON object to JSON string

            });
            const data3 = await response.json();
            let totalCapLoans = data3.total;
            let totalCapLoansField = document.getElementById("totalCapLoans");
            totalCapLoansField.innerHTML = totalCapLoans;

            // fill in all other spaces
            let totalLoansField = document.getElementById("totalLoans");
            totalLoansField.innerHTML = totalLoans;
            let savedGracePeriodField = document.getElementById("whatIfPaid");
            savedGracePeriodField.textContent = savedGracePeriod;
            let savedAllYearsField = document.getElementById("whatIfSaved");
            savedAllYearsField.textContent = savedAllYears;


            toggleResults("unsubResultsContainer", "subResultsContainer");
            resultsContainer = document.getElementById("unsubResultsContainer");
        } else {
            // fill in all other spaces
            let totalLoansField = document.getElementById("totalLoansSub");
            totalLoansField.innerHTML = totalLoans;
            let savedGracePeriodField = document.getElementById("whatIfPaid");
            savedGracePeriodField.textContent = savedGracePeriod;
            let savedAllYearsField = document.getElementById("whatIfSaved");
            savedAllYearsField.textContent = savedAllYears;

            toggleResults("subResultsContainer", "unsubResultsContainer");
            resultsContainer = document.getElementById("subResultsContainer");
        }

        // Scroll to the results section every time
        resultsContainer.scrollIntoView({ behavior: "smooth", block: "start" });

        confetti({
            particleCount: 150,
            spread: 120,
            colors: ['#C7E9C0', '#005A32', '#74C478'],
            origin: { y: 0.8 },
          });

    }
    catch (error) {
        console.error("Error in Calculating Interest:", error);
    }
});


// CALCULATIONS UPLOAD
document.getElementById("loanForm").addEventListener("submit", async function(event) {
    event.preventDefault();  // Prevent default form submission
    const resultsContainer = document.getElementById("resultContainer");

    // save graduation date from input field
    const gradDate = document.getElementById("graduationDate2").value;

    // save each loan information into an array
    loans = [] 
    // select all fieldsets in loan container and loop through each loan
    document.querySelectorAll(".loanEntry").forEach((loanEntry, index) => {
        const balance = loanEntry.querySelector('input[name="balance[]"]').value;
        const interest = loanEntry.querySelector('input[name="interest[]"]').value;
        const type = loanEntry.querySelector('select[name="type[]"]').value;
        const received = loanEntry.querySelector('select[name="semester[]"]').value;

        // create JSON object and add to loans
        loans.push({
            loanNum: index + 1,
            principal: parseFloat(balance),
            interest: parseFloat(interest),
            type: type,
            semReceived: received
        })
    });

    //Call Python function with API request
    try {
        // Fetch CSRF token and include in request
        const csrfToken = getCSRFToken();
        const response = await fetch("/upload_calculation/", {
            //HTTP request settings to send data to the backend as JSON
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken  // Include CSRF token in request headers
            },
            body: JSON.stringify({gradDate, loans}) //converts JSON object to JSON string
        });

        //if there is an error with request, throw error
        // if (!response.ok) throw new Error("Failed to save interest calculation");
    }
    catch (error) {
        console.error("Error in Calculating Interest:", error);
    }
});

// connection to recommendations button
document.getElementById("whatIfForm").addEventListener("submit", async function(event) {
    event.preventDefault();  // Prevent default form submission

    // save custom payment selected by the user
    const customPayment = document.getElementById("customPayment").value;

    const resultsContainer = document.getElementById("resultContainer");

    // save graduation date from input field
    const gradDate = document.getElementById("graduationDate2").value;

    // save each loan information into an array
    loans = [] 
    // select all fieldsets in loan container and loop through each loan
    document.querySelectorAll(".loanEntry").forEach((loanEntry, index) => {
        const balance = loanEntry.querySelector('input[name="balance[]"]').value;
        const interest = loanEntry.querySelector('input[name="interest[]"]').value;
        const type = loanEntry.querySelector('select[name="type[]"]').value;
        const received = loanEntry.querySelector('select[name="semester[]"]').value;

        // create JSON object and add to loans
        loans.push({
            loanNum: index + 1,
            principal: parseFloat(balance),
            interest: parseFloat(interest),
            type: type,
            semReceived: received
        })
    });

    
    //Call Python function with API request
    try {
        // Fetch CSRF token and include in request
        const csrfToken = getCSRFToken();
        // frontend calls server endpoint with url calculate_interest
        const response = await fetch("/calculate_whatif", {
            //HTTP request settings to send data to the backend as JSON
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken  // Include CSRF token in request headers
            },
            body: JSON.stringify({gradDate, loans, customPayment}) //converts JSON object to JSON string
        });

        //if there is an error with request, throw error
        if (!response.ok) throw new Error("Failed to fetch what if calculation");
        
        // parses response body as JSON
        const data = await response.json();

        //extracts value in returned dictionary
        const savedGracePeriod = data.savedGracePeriod;
        const savedAllYears = data.savedAllYears;
        const isLargerPayment = data.isLargerPayment;

        // Location to fill in what if value
        let savedGracePeriodField = document.getElementById("whatIfPaid");
        savedGracePeriodField.textContent = savedGracePeriod;
        let savedAllYearsField = document.getElementById("whatIfSaved");
        savedAllYearsField.textContent = savedAllYears;

        // if isLargerPayment is true -> create another message popup with a disclaimer

        // Make results and recommendations containers visible
        document.querySelector("#resultContainer .d-none")?.classList.remove("d-none");
        document.querySelector("#recommendationsContainer .d-none")?.classList.remove("d-none");

        // Scroll to the results section every time
        resultsContainer.scrollIntoView({ behavior: "smooth", block: "start" });

    }
    catch (error) {
        console.error("Error in Calculating Interest:", error);
    }
});