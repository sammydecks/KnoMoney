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
            popover: { title: 'Add Loans', description: 'Add any additional student loans to accurately calculate total interest.' }, 
            disableActiveInteraction: true,
        },
        { 
            element: '#calculate', 
            popover: { title: 'Calculate!', description: 'Click Calculate when you finish adding your loans!' },
            disableActiveInteraction: true, 
        }
    ]
  });
  
  document.addEventListener("DOMContentLoaded", () => {
    const btnRedirect = document.querySelector("#tourRedirect");
    if (btnRedirect) {
        btnRedirect.addEventListener("click", () => {
            sessionStorage.setItem("startTour", "true");
        });
    }

    const btnRestart = document.querySelector("#tourRestart");
    if (btnRestart) {
        btnRestart.addEventListener("click", () => {
            driverObj.drive(); // Restart tutorial manually
        });
    }

    // If sessionStorage flag is set, start tour on calculator page
    if (sessionStorage.getItem("startTour") === "true") {
        driverObj.drive();
        sessionStorage.removeItem("startTour"); // Prevent running again on refresh
    }
});

