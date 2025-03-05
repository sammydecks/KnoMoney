import pandas as pd
import math
from datetime import datetime, date

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
    loans['balance'] = loans['principal'] #create new row for the balance to calculate monthly payments based on if student paids off all simple interest
    results["totalSaved"] = calculateTotalSaved(gradDate, loans)


    # calculate monthly payments for recommendation
    results["monthlyPay"] = calculateMonthlyIntPay(gradDate, loans)

    # calculate whatIf calculations
    # the "Calculate" button will populate with $25/month as the what if recommendation
    payment = 25
    whatIfResults = calculateWhatIf(gradDate, loans, payment)
    results.update({ "savedGracePeriod": whatIfResults["savedGracePeriod"], "savedAllYears": whatIfResults["savedAllYears"] })

    print(results)
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
            # calculate the number of days that have passed from date received to end of grace period(unsubsidized accrues daily) 
            days = (gradDate - pd.to_datetime(loans.loc[l]['dateReceived'])).days + 180 
            
            # calculate the total interest accrue
            # equation: interest = principle * (interest rate) / 365 * days
            interest = loans.loc[l]['principal'] * (loans.loc[l]['interest'])/365 * days
        
            # add the interest to the total interest paid
            totalInt += interest
        
    totalInt = round(float(totalInt), 2) #cast to float and round to 2 decimal places
    return totalInt



def calculateTotalSaved(gradDate, loans, years=10):
    '''
    Parameters:
    ----------
    gradDate (datetime): graduation date
    loans (pd df): 
        [loanNum: int,
        principal: float,
        interest: float,
        type: enum (subsidized, unsubsidized)
        dateReceived: datetime,
        monthlyPay: float]
    years (int): number of years expected to take to pay off entire student loan (default=10 years)
    
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

    loans = calculateIndMonthlyPay(loans, years) #creates a new row in loans (monthlyPay: float) that will be used in the calculation below to see total saved

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
            totalPaid = monthPayments * n
            # calculate total amount that could have been save on the single unsubsidized loan and add to totalSave
            totalSaved += totalPaid - (loans.loc[l]['monthlyPay'] * n) #totalSaved = total paid (if interest NOT paid)  - total paid (if interest paid)

    totalSaved = round(float(totalSaved), 2) #cast to float and round to 2 decimal places
    return totalSaved


def calculateMonthlyIntPay(gradDate, loans):
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
    monthlyPay (float): amount to pay each month to simple accrued interest
    '''
    
    '''
    The logic: 
    - The total interest accrued is calculated
    - The current date from today until graduation is calculate
    - ASSUMING that no simple accrued payment has been paid off, the total interest is divided by remaining months (rounded down) to calculate monthly pay
    - NOTE: the remaining months does include the grace period
    '''

    # calculate total interest from receiving loans to graduation
    totalInterest = calculateInterest(gradDate, loans)

    # calculate time until end of grace period from today and round down to nearest month (approximating a month with 30 days)
    timeTillGrace= math.floor((gradDate - pd.to_datetime(date.today())).days / 30) + 6 

    monthlyPay = round(float(totalInterest / timeTillGrace), 2) #cast to float and round to 2 decimal places

    return monthlyPay


def calculateWhatIf(gradDate, loans, payment):
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
    whatIfResults (pd df):
        [savedGracePeriod: float,
        savedAllYears: float]    
    '''

    '''
    The logic:
    - the user can input a payment more or less than the recommended monthly payment
    - if payment < monthlyPay:
        - payment will first go to interest -> calculate remaining unpaid interest that will then be capitalized 
        - calculate monthly interest for each loan
        - calculate proportion of interest for each loan
        - multiply each proportion with total remaining balance
        - add the proportion of interest capitalized onto the principal
        - calculate total debt amount paid with the new capitalized principal
        - calculate total debt amount paid with the higher capitalized principal (if simple accrued interest was never paid)
        - calculate the difference saved 
    - if payment > monthlyPay:
        - ASSUMING default payment allocation
        - Remaining payment will be paid proportionally across all UNSUBSIDIZED loans' principals
        - After paying extra for the first month, the principal decreases, causing the interest to decrease -> more of the monthly payment will go towards principal
        - This will continue until the end of the grace period to calculate the new lowered principal
        - calculate total debt amount paid with new lowered principal (if new lowered principal is negative somehow -> change to just 0)
        - calculate total debt amount paid with higher capitalized principal (if simple accrued interest was never paid)
        - calculate the difference saved
    - calculate total paid by end of grace period (payment * (months left until graduation + 6))
        
    '''

    # total monthly interest payment in order to not have any interest capitalized
    totalMonthlyIntPay = calculateMonthlyIntPay(gradDate, loans)

    # initialize df to return
    whatIfResults = {
        "savedGracePeriod": 0,
        "savedAllYears": 0
    }
    # add new column initialized to 0
    loans['balance'] = 0

    n = math.floor((gradDate - pd.to_datetime(date.today())).days / 30) + 6 #number of monthly payments from today till end of grace period 

    # calculate savedGracePeriod
    whatIfResults['savedGracePeriod'] = payment * n

    # calculate total saved all years
    if payment < totalMonthlyIntPay:

        # remaining amount that is not paid off by end of grace period
        unpaidInterest = (totalMonthlyIntPay - payment) * n

        # loop through each loan and set the new balance (original principal + prop(unpaidInterest))
        for l in range(len(loans)):
            # current loan
            currLoan = loans.loc[l]

            if currLoan['type'] == "unsubsidized":
                # calculate monthly interest accrued for given loan 
                currMonthlyInt = currLoan['principal'] * (currLoan['interest'])/365 * 30
                # calculate proportion of unpaidInterest that will be added to original principal to create new balance
                currLoan['balance'] = (currMonthlyInt/totalMonthlyIntPay) * unpaidInterest + currLoan['principal']
            elif currLoan['type'] == "subsidized":
                currLoan['balance'] = currLoan['principal']

        # after calculating the new balance for every loan, calculate total saved over 10 years
        whatIfResults['savedAllYears'] = calculateTotalSaved(gradDate, loans)
    
    elif payment > totalMonthlyIntPay:
        # calculate extra payment that can go towards paying principal
        extraPayment = payment - totalMonthlyIntPay
        # initialize new row of balance = principal
        loans['balance'] = loans['principal']

        # calculate total loan principal for unsubsidized loans (this will help with proportions later)
        unsubsidizedLoans = loans[loans['type'] == 'unsubsidized']
        totalUnsubsidizedPrincipal = unsubsidizedLoans['principal'].sum()

        # iterate through n payments, recalculating extra payment and reducing 

        # TODO: implement this
        whatIfResults['savedAllYears'] = -1
    
    # else payment = monthlyPay -> this means that the balance that monthly pay is calculated off on = original principal
    else: 
        loans['balance'] = loans['principal']
        whatIfResults['savedAllYears'] = calculateTotalSaved(gradDate, loans)
    
    return whatIfResults

def calculateIndMonthlyPay(loans, years):
    '''
    Parameters:
    ----------
    loans (pd df): 
        [loanNum: int,
        principal: float,
        interest: float,
        type: enum (subsidized, unsubsidized),
        dateReceived: datetime,
        balance: float]
    years (float): number of years expected to take to pay off entire student loan (default=10 years)
    
    Return:
    ------
    loans (pd df): 
        [loanNum: int,
        principal: float,
        interest: float,
        type: enum (subsidized, unsubsidized),
        dateReceived: datetime,
        balance: float
        monthlyPay: float]  
    '''

    ''' 
    The logic:
    - Using the starting balance after the grace period 
        (balance=principal if all the accrued interest is paid - using balance will help use this method if principal changes due to payments while in school)
    - Calculate the monthly payment and add as a new column in df
    '''

    # add new column initialized to 0
    loans['monthlyPay'] = 0

    for l in range(len(loans)):
        # current loan
        currLoan = loans.loc[l]

        # calculate monthly payments
        # A = P * (r(1+r)^n)/((1+r)^n-1) 
        # P = loan principal, r = monthly interest rate (annual R/12), n=total payments (x years * 12)
        r = (currLoan['interest']/100) / 12
        n = years * 12
        
        # makes sure r is not = 0
        # TODO: check and test this calculation
        if r > 0:
            monthPayments = currLoan['balance'] * (r * (1+r)**n) / ((1+r)**n - 1)
        else:
            monthPayments = currLoan['balance'] / n
        
        # set monthlyPay value for given row
        loans.loc[l]['monthlyPay'] = round(float(monthPayments), 2)
    
    return loans


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

    
