const driver = window.driver.js.driver;

const driverObj = driver({
    showProgress: true,
    steps: [
        { 
            element: '#graduation', 
            popover: { title: 'Expected Graduation Date', description: 'Enter your expected graduation date.' } 
        },
        { 
            element: '#balance', 
            popover: { title: 'Loan Balance', description: 'Enter the balance of the initial loan.' } 
        },
        { 
            element: '#interest', 
            popover: { title: 'Loan Interest Rate', description: 'Enter the interst rate. The federal rate changes each year!' } 
        },
        { 
            element: '#type', 
            popover: { title: 'Loan Type', description: 'Enter if the loan is subsidized or unsubsidized.' } 
        },
        { 
            element: '#received', 
            popover: { title: 'Date Loan Received', description: 'Enter the date the loan was taken out.' } 
        },
        { 
            element: '#addLoan', 
            popover: { title: 'Add Loans', description: 'Add any additional student loans to accurately calculate total interest.' } 
        },
        { 
            element: '#calculate', 
            popover: { title: 'Calculate!', description: 'Click Calculate when you finish adding your loans!' } 
        }
    ]
  });
  
document.addEventListener("DOMContentLoaded", () => {
    const btnTour = document.querySelector("#tour");

    if (btnTour) {
        btnTour.addEventListener("click", () => {
            // Set a start tour flag before navigating to calculator page
            sessionStorage.setItem("startTour", "true");
        });
    }

    // Check if we're on the calculator page and if the tour should run
    if (sessionStorage.getItem("startTour") === "true") {
        sessionStorage.removeItem("startTour"); // Remove the flag so it doesn't run again
        driverObj.drive();
    }
});

