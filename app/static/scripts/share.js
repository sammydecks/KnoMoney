const sendTrackingData = (action) => {
    fetch("/track-action/", {  // Adjust URL if needed
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ action }),
    }).then(response => response.json())
      .then(data => console.log("Tracking Response:", data))
      .catch(error => console.error("Error tracking action:", error));
};


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("emailButton").addEventListener("click", function(event) {
        // Prevent default behavior to handle the click
        event.preventDefault();
        
        // Get the savings amount (this assumes you have the savings amount in a class called 'savingsAmt')
        let savingsAmount = document.querySelector(".savingsAmt").innerText; 
        
        // Recipient email from the input field
        let recipientEmail = document.getElementById("shareEmail").value;  // Assuming 'shareEmail' is the input ID
        
        // Check if email is provided
        if (!recipientEmail) {
            console.warn("Recipient email is required");
            alert("Please provide a recipient email address.");
            return;
        }
    
        // Email subject and body content
        let emailSubject = "Potential Student Loan Savings";
        let emailBody = 
            "Hi,\n\n" +
            "I wanted to share some important information about saving money on student loans.\n\n" +
            `Based on the selected loan range, there is potential to save ${savingsAmount} by paying accrued interest before it capitalizes.\n\n` +
            "Here's how it works:\n" +
            "- While in school, interest accrues on unsubsidized loans.\n" +
            "- If unpaid, this interest is added to the loan balance after graduation, increasing future costs.\n" +
            "- By paying off accrued interest early, you can reduce your total repayment amount and lower long-term costs.\n\n" +
            "Learn more and explore tools to help at KnoMoney: https://www.knomoney.com\n\n" +
            "Additional resources:\n" +
            "- FAQ: https://www.knomoney.com/faqs/\n";
    
        // Construct the mailto link
        let mailtoLink = `mailto:${recipientEmail}?subject=${encodeURIComponent(emailSubject)}&body=${encodeURIComponent(emailBody)}`;
    
        // Update the href of the button to the mailto link
        this.setAttribute("href", mailtoLink);
    
        // Trigger the mailto link (opens the default email client)
        window.location.href = mailtoLink;

        // POST
        sendTrackingData("email_share");
    });
    
    

    document.getElementById("copyButton").addEventListener("click", function() {
        let textToCopy = document.querySelector("#share").innerText;
        let copyIcon = document.getElementById("copyIcon");
    
        navigator.clipboard.writeText(textToCopy).then(() => {
            // Change icon to clipboard-check
            copyIcon.classList.remove("bi-clipboard");
            copyIcon.classList.add("bi-clipboard-check");
    
            // Update tooltip message
            this.setAttribute("title", "Copied!");
    
            // Reset icon and tooltip after 2 seconds
            setTimeout(() => {
                copyIcon.classList.remove("bi-clipboard-check");
                copyIcon.classList.add("bi-clipboard");
                this.setAttribute("title", "Copy to clipboard");
            }, 3000);
        });

        // POST
        sendTrackingData("copy_to_clipboard");
    });
});