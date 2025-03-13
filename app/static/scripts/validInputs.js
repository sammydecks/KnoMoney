document.addEventListener("DOMContentLoaded", function () {
    const graduationDateInput = document.getElementById("graduationDate");

    // Get today's date and format it as YYYY-MM 
    let today = new Date();
    let minMonth = today.toISOString().slice(0, 7); // Extract YYYY-MM format

    graduationDateInput.setAttribute("min", minMonth); // Set min to current or future months
});
