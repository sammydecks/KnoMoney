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
});
