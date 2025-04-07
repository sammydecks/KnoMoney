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
        let email = document.getElementById("friendEmail").value;
    
        if (!email) {
            console.warn("Missing email.");
            return;
        }
    
        try {
            const csrfToken = getCSRFToken();
    
            const response = await fetch("/upload_referral/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({email})
            });
    
            if (!response.ok) throw new Error("Failed to save referral email");
    
            // Success! Now draft email.
            const subject = encodeURIComponent("Check out KnoMoney!");
            const body = encodeURIComponent("Hey, I found KnoMoney, a website that helps you learn how you can save money on your student loan interest. I thought you would be a great candidate to check it out: https://www.knomoney.com");
    
            window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
    
        } catch (error) {
            console.error("Error in Saving Email", error);
        }
    });    
});
