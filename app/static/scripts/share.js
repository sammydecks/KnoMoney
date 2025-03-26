document.addEventListener("DOMContentLoaded", function () {
    // Share via email
    document.getElementById("emailButton").addEventListener("click", function() {
        let textToShare = document.querySelector("#share").innerText;
        let emailBody = encodeURIComponent(textToShare);
        let mailtoLink = `mailto:?subject=Potential Student Loan Savings&body=${emailBody}`;
        this.setAttribute("href", mailtoLink);
    });

    document.getElementById("copyButton").addEventListener("click", function() {
        let textToCopy = document.querySelector("#share").innerText; 
        navigator.clipboard.writeText(textToCopy).then(() => {
            let message = document.getElementById("copyMessage");
            message.classList.remove("d-none");
            setTimeout(() => message.classList.add("d-none"), 2000);
        });
    });
});
