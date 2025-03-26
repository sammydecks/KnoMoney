import pandas as pd
import math
from datetime import datetime, date
from enum import Enum


# Define the Enum for loan ranged
class LoanRangeEnum(Enum):
    range1 = "~ $10K"
    range2 = "~ $20K"
    range3 = "~ $30K"
    range4 = "~ $40K"

# Basic Results populated 
def calculateSimpleResults(gradDate, loanRange: LoanRangeEnum):
    '''
    Parameters:
    ----------
    gradDate (datetime): graduation date (The first day of the given MM/YYYY)
    loanRange (enum): a range of loans that can be selected
        [range1 (0-10k),
        range2 (10-20k)
        range3 (20-30k),
        range4 (30k+)]
    
    Return:
    ------
    totalSaved (int): total amount potentially saved (rounded up to nearest $100)
    '''

    ''' 
    ASSUMPTIONS:
    dateReceived of the Loan = disbursed 1-4 years in the past on Aug. 1
    interest (r) = current interest of 2024-25 loan: 6.53% used for all future years
    loans = takes the higher range (if range4 -> make 50k)
    '''
    # source: https://finaid.org/loans/historicalrates/
    # only going 4 years back from current implementation (in 2025)
    r = {
        2024: 0.0653,
        2023: 0.055,
        2022: 0.0499,
        2021: 0.0373,
    }
    currInt = 0.0653
    n = 120 #over 10 years (120 months)

    # Set loan amount based on the enum
    # NOTE: dividing all the values by 4 to estimate about a fourth of the loans are unsubsidized
    loanAmt = {
        LoanRangeEnum.range1.value: 10000/4,
        LoanRangeEnum.range2.value: 20000/4,
        LoanRangeEnum.range3.value: 30000/4,
        LoanRangeEnum.range4.value: 50000/4, #Assume $50 for highest range
    }.get(loanRange.value, 0) #Default to 0 if something goes wrong

    # Estimate yearly loan takeout across 4 years
    loanAmtPerYear = loanAmt / 4

    # Estimate date dispursement
    gradYear = gradDate.year
    gradMonth = gradDate.month
    loanStartYears = [
        datetime(gradYear - 4, 8, 1),  # 4 years ago Aug. 1
        datetime(gradYear - 3, 8, 1),  # 3 years ago
        datetime(gradYear - 2, 8, 1),  # 2 years ago
        datetime(gradYear - 1, 8, 1)   # 1 year ago
    ]
    if gradMonth > 8:
        loanStartYears = [
            datetime(gradYear - 3, 8, 1),  # 3 years ago Aug. 1
            datetime(gradYear - 2, 8, 1),  # 2 years ago
            datetime(gradYear - 1, 8, 1),  # 1 year ago
            datetime(gradYear, 8, 1)   # several months ago Aug. 1
        ]


    # Estimate total interest accrued based on staggered loan disbursement
    totalInt = 0
    for startDate in loanStartYears:
        # Calculate the number of months between loan disbursement and graduation
        months_since_start = (gradYear - startDate.year) * 12 + (gradMonth - startDate.month)
        months_since_start = max(months_since_start, 0) #make sure months is non-negative
        
        # Calculate simple interest for each loan year
        intRate = r.get(startDate.year, currInt) #default to 2024-25 interest rate (6.53%) for all future years
        totalInt += intRate * loanAmtPerYear * months_since_start / 12  # Interest for the exact number of months

    # calculate total debt with interest capitalized
    totalDebtInt = (loanAmt + totalInt) * (currInt * (1+currInt)**n) / ((1+currInt)**n - 1) * n

    # calculate total debt without interest capitalized
    totalDebtNoInt = loanAmt * (currInt * (1+currInt)**n) / ((1+currInt)**n - 1) * n

    # subtract to see potential savings
    totalSaved = int(round(totalDebtInt - totalDebtNoInt, -2))

    return totalSaved

