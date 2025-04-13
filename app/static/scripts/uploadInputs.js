// Function to get CSRF token from cookies
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}

// Save Emails
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
    
            const response = await fetch("/upload_emaillist/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({email})
            });
    
            if (!response.ok) throw new Error("Failed to save email");
    
            // Success! Now draft email.
            const subject = encodeURIComponent("You’re on the KnoMoney Path! 🎓💰");
            const body = encodeURIComponent(
                `Hey there!

                You just joined the KnoMoney crew — thanks for being part of a growing community of students learning how to save smarter on student loans. We'll keep you posted with more helpful tools, updates, and tips so you can stay ahead of the game. Until then, you can revisit KnoMoney anytime at: https://www.knomoney.com

                - The KnoMoney Team 💚`
            );
            window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
    
        } catch (error) {
            console.error("Error in Saving Email", error);
        }
    });    
});


