import numpy as np
import pandas as pd

def calculateInterest(gradDate, loans):
    '''
    Parameters:
    ----------
    gradDate (datetime): graduation date
    loans (pd df): 
        [loanNum: int,
        principal: float,
        interest: float,
        subsidized: int (0 or 1),
        dateReceived: datetime]
    
    Return:
    ------
    totalInt (float): total interest paid
    '''
    totalInt = 0
    
    # iterate through each loan
    for l in range(len(loans)):
        # if the loan is unsubsidized, calculate the interest
        if loans.loc[l]['subsidized'] == 0:
            # calculate the number of days that have passed (unsubsidized accrues daily)
            days = (gradDate - loans.loc[l]['dateReceived']).days
            
            # calculate the total interest accrue
            # equation: interest = principle * (interest rate) / 365 * days
            interest = loans.loc[l]['principal'] * (loans.loc[l]['interest'])/365 * days
        
            # add the interest to the total interest paid
            totalInt += interest
        
    return totalInt


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
                          'subsidized': [1, 1, 0],
                          'dateReceived': [date1, date2, date3]})

    print((gradDate-date3).days)
    print(calculateInterest(gradDate, test1)) 