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
    document.querySelectorAll(".semester").forEach(select => {
        populateSemesterDropdown(select);
    });
}

function populateSemesterDropdown(select) {
    const startYear = 2015;
    const endYear = 2024;
    const semesters = ["Fall", "Summer", "Spring"];

    select.innerHTML = '<option value="" disabled selected>-- select --</option>'; // Clear any existing options
    
    // add Spring 2025
    let option = document.createElement("option");
    option.value = `Spring 2025`;
    option.textContent = `Spring 2025`;
    select.appendChild(option);

    // all semester 2015 - 2024
    for (let year = endYear; year >= startYear; year--) {
        semesters.forEach(semester => {
            let option = document.createElement("option");
            option.value = `${semester} ${year}`;
            option.textContent = `${semester} ${year}`;
            select.appendChild(option);
        });
    }
}
