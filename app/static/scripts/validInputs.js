document.addEventListener("DOMContentLoaded", function () {
    // simple calc validation
    const graduationDateInput = document.getElementById("graduationDate");
    const graduationDateInput2 = document.getElementById("graduationDate2");

    // Get today's date and format it as YYYY-MM 
    let today = new Date();
    let minMonth = today.toISOString().slice(0, 7); // Extract YYYY-MM format

    graduationDateInput.setAttribute("min", minMonth); // Set min to current or future months
    graduationDateInput2.setAttribute("min", minMonth);

    // Populate semester dropdown options
    populateSemesterDropdowns();
});


function populateSemesterDropdowns() {
    const startYear = 2015;
    const endYear = 2025;
    const semesters = ["Spring", "Summer", "Fall"];
    
    document.querySelectorAll(".semester").forEach(select => {
        select.innerHTML = '<option value="" disabled selected>-- select --</option>'; // Clear existing options

        for (let year = startYear; year <= endYear; year++) {
            semesters.forEach(semester => {
                let option = document.createElement("option");
                option.value = `${semester} ${year}`;
                option.textContent = `${semester} ${year}`;
                select.appendChild(option);
            });
        }
    });
}