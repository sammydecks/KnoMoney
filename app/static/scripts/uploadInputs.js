// Function to get CSRF token from cookies
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

// Save Referral Emails
document.addEventListener("DOMContentLoaded", function () {
    // send button next to "share with a friend" input
    document.getElementById("sendEmail").addEventListener("click", async function(event) {
        // if email not filled, return empty
        let email = document.getElementById("friendEmail").value;
        if (!email) {
            console.warn("Missing email.");
            return;
        }
        //Call Python function with API request
        try {
            // Fetch CSRF token and include in request
            const csrfToken = getCSRFToken();
            // frontend calls server endpoint with url calculate_interest
            const response = await fetch("/upload_referral/", {
                //HTTP request settings to send data to the backend as JSON
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken  // Include CSRF token in request headers
                },
                body: JSON.stringify({email}) //converts JSON object to JSON string
            });

            //if there is an error with request, throw error
            if (!response.ok) throw new Error("Failed to save referral email");
        }
        catch (error) {
            console.error("Error in Saving Email", error);
        }
    });
});
