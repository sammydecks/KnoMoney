import pandas as pd

# This function calculates ALL the results and recommendations when the user clicks "Calculate" on the calculator page
def calculateResults(gradDate, loans):
    results = {
        "totalInterest": 0,
        "totalSaved": 0,
        "monthlyPay": 0,
        "savedGracePeriod": 0,
        "saved10Years": 0
    }

    results["totalInterest"] = calculateInterest(gradDate, loans)
    results["totalSaved"] = calculateTotalSaved(gradDate, loans)

    return 0



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



def calculateTotalSaved(gradDate, loans):
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
    totalSaved (float): total interest paid
    '''
    totalSaved = 0
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
            totalSaved += interest

    return totalSaved


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
                          'type': [1, 1, 0],
                          'dateReceived': [date1, date2, date3]})

    print((gradDate-date3).days)
    print(calculateInterest(gradDate, test1)) 

