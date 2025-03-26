document.addEventListener("DOMContentLoaded", function () {
    const shareButton = document.getElementById("shareButton");
    const popup = document.getElementById("sharePopup");
    const closePopup = document.getElementById("closePopup");

    shareButton.addEventListener("click", function () {
        popup.classList.remove("d-none"); // Show popup

        // Log the event via an HTTP request
        fetch("log-share", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                event: "share_clicked",
                timestamp: new Date().toISOString()
            })
        }).catch(error => console.error("Error logging share:", error));
    });

    closePopup.addEventListener("click", function () {
        popup.classList.add("d-none"); // Hide popup when Close is clicked
    });

    // Share via email
    document.getElementById("emailButton").addEventListener("click", function() {
        let textToShare = document.querySelector("#sharePopup .border").innerText;
        let emailBody = encodeURIComponent(textToShare);
        let mailtoLink = `mailto:?subject=Potential Student Loan Savings&body=${emailBody}`;
        this.setAttribute("href", mailtoLink);
    });

    document.getElementById("copyButton").addEventListener("click", function() {
        let textToCopy = document.querySelector("#sharePopup .border").innerText; 
        navigator.clipboard.writeText(textToCopy).then(() => {
            let message = document.getElementById("copyMessage");
            message.classList.remove("d-none");
            setTimeout(() => message.classList.add("d-none"), 2000);
        });
    });
});
