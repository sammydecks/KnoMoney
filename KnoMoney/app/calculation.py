import pandas as pd

# This function calculates ALL the results and recommendations when the user clicks "Calculate" on the calculator page
def calculateResults(gradDate, loans):
    '''
    Parameters:
    ----------
    gradDate (datetime): graduation date
    loans (pd df): 
        [loanNum: int,
        principal: float,
        interest: float,
        type: enum (subsidized, unsubsidized)
        dateReceived: datetime]
    
    Return:
    ------
    results (dictionary): all results that will populate the calculator page
        [totaInterest: float,
        totalSaved: float,
        monthlyPay: float,
        savedGracePeriod: float,
        savedAllYears: float]
    '''

    results = {
        "totalInterest": 0,
        "totalSaved": 0,
        "monthlyPay": 0,
        "savedGracePeriod": 0,
        "savedAllYears": 0
    }

    # calculate total simple interest that would be accrued from time loan is taken out to graduation date
    results["totalInterest"] = calculateInterest(gradDate, loans)

    # calculate total saved under the assumption that the loan is on a 10 year repayment plan
    years = 10 
    results["totalSaved"] = calculateTotalSaved(gradDate, loans, years)


    # calculate monthly payments for recommendation
    results["monthlyPay"] = calculateMonthlyPay(gradDate, loans)

    # calculate whatIf calculations
    # the "Calculate" button will populate with $25/month as the what if recommendation
    payment = 25
    whatIfResults = calculateWhatIf(gradDate, loans, payment)
    results.update({ "savedGracePeriod": whatIfResults["savedGracePeriod"], "savedAllYears": whatIfResults["savedAllYears"] })
    
    return results



def calculateInterest(gradDate, loans):
    '''
    Parameters:
    ----------
    gradDate (datetime): graduation date
    loans (pd df): 
        [loanNum: int,
        principal: float,
        interest: float,
        type: enum (subsidized, unsubsidized)
        dateReceived: datetime]
    
    Return:
    ------
    totalInt (float): total interest paid
    '''
    totalInt = 0
    
    # iterate through each loan
    for l in range(len(loans)):
        # if the loan is unsubsidized, calculate the interest
        if loans.loc[l]['type'] == "unsubsidized":
            # calculate the number of days that have passed (unsubsidized accrues daily)
            days = (gradDate - pd.to_datetime(loans.loc[l]['dateReceived'])).days
            
            # calculate the total interest accrue
            # equation: interest = principle * (interest rate) / 365 * days
            interest = loans.loc[l]['principal'] * (loans.loc[l]['interest'])/365 * days
        
            # add the interest to the total interest paid
            totalInt += interest
        
    totalInt = round(totalInt, 2)
    return totalInt



def calculateTotalSaved(gradDate, loans, years):
    '''
    Parameters:
    ----------
    gradDate (datetime): graduation date
    loans (pd df): 
        [loanNum: int,
        principal: float,
        interest: float,
        type: enum (subsidized, unsubsidized)
        dateReceived: datetime]
    years (int): number of years expected to take to pay off entire student loan
    
    Return:
    ------
    totalSaved (float): total interest paid
    '''

    '''
    The logic:
    - Unsubsidized federal loans accrue daily simple (NOT compounding) interest even while a student is still in college
    - After graduation, students will have a 6 month grace period before repayment starts
        - This means that there is still daily simple interest from graduate to the end of the 6 month grace period
        - NOTE: this calculation uses 180 days instead of 6 months for a close estimate 
    - After the 6 month grace period, all the interest that has been acrued will be added to the original principal (aka capitalized) to create a new principal
    - This new principal will have monthly simple (NOT compounding) interest

    - The calculation first looks for every unsubsidized loan and calculates what this new principal would be if a student never paid their interest during school/grace period
    - Then the monthly payments that would be made is calculated
    - This monthly payment is multiplied with x years to find the total amount of money that was actually paid
    - This total paid value is subtracted with the original principal to result in the total amount saved for that single unsubsidized loan if the student paid off that daily simple interest
    - This is summed across all unsubsidized loans
    '''
    totalSaved = 0
    # iterate through each loan
    for l in range(len(loans)):
        # current loan
        currLoan = loans.loc[l]

        # if the loan is unsubsidized, calculate the interest
        if currLoan['type'] == "unsubsidized":
            # calculate the number of days between start of loan and end of grace period (unsubsidized accrues daily)
            days = (gradDate - pd.to_datetime(currLoan['dateReceived'])).days + 180 #add 180 for the approx. 6 month grace period
            
            # calculate the total interest accrue
            # equation: interest = principle * (interest rate) / 365 * days
            interest = currLoan['principal'] * (currLoan['interest'])/365 * days
        
            # calculate new principal (if previous interest is accrued)
            # add the interest to the total interest paid
            newPrincipal = currLoan['principal'] + interest

            # calculate monthly payments
            # A = P * (r(1+r)^n)/((1+r)^n-1) 
            # P = loan principal, r = monthly interest rate (annual R/12), n=total payments (x years * 12)
            r = (currLoan['interest']/100) / 12
            n = years * 12
            
            # makes sure r is not = 0
            # TODO: check and test this calculation
            if r > 0:
                monthPayments = newPrincipal * (r * (1+r)**n) / ((1+r)**n - 1)
            else:
                monthPayments = newPrincipal / n
            # calculate the total amount paid over x years
            totalPaid = monthPayments * years
            # calculate total amount that could have been save on the single unsubsidized loan and add to totalSave
            totalSaved += totalPaid-currLoan['principal']

    return totalSaved


def calculateMonthlyPay(gradDate, loans):
    
    return 0


def calculateWhatIf(gradDate, loans, payment):

    whatIfResults = {
        "savedGracePeriod": 0,
        "savedAllYears": 0
    }
    return whatIfResults


# main method
if __name__ == "__main__":
    date1 = pd.to_datetime('2022-08-01')
    date2 = pd.to_datetime('2023-08-01')
    date3 = pd.to_datetime('2024-08-01')
    gradDate = pd.to_datetime('2025-05-01')
    
    int1 = 0.0499 #22-23
    int2 = 0.055 #23-24
    int3 = 0.0653 #24-25
    test1 = pd.DataFrame({'loanNum': [1, 2, 3],
                          'principal': [1000, 2000, 3000],
                          'interest': [int1, int2, int3],
                          'type': ["subsidized", "subsidized", "unsubsidized"],
                          'dateReceived': [date1, date2, date3]})

    print((gradDate-date3).days)
    # print(calculateInterest(gradDate, test1)) 
    print("Results")
    print(calculateResults(gradDate, test1))
