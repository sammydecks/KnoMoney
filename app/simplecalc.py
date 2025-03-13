import pandas as pd
import math
from datetime import datetime, date

# Basic Results populated 
def calculateSimpleResults(gradDate, loanRange):
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
    dateReceived of the Loan = 4 exact years prior
    interest (r) = current interest of 2024-25 loan: 6.53%
    loans = takes the higher range (if range4 -> make 50k)
    '''
    r = 0.0653
    n = 120 #over 10 years (120 months)

    loanAmt = 10000
    # set loan amount
    if (loanRange == 'range2'):
        loanAmt = 20000
    elif (loanRange == 'range3'):
        loanAmt = 30000
    elif (loanRange == 'range4'):
        loanAmt = 50000

    # calculate accrued simple interest if loan amount taken out 4 years ago (NOT ACCURATE)
    totalInt = r * loanAmt * 4

    # calculate total debt with interest capitalized
    totalDebtInt = (loanAmt + totalInt) * (r * (1+r)**n) / ((1+r)**n - 1) * n

    # calculate total debt without interest capitalized
    totalDebtNoInt = loanAmt * (r * (1+r)**n) / ((1+r)**n - 1) * n

    # subtract to see potential savings
    totalSaved = totalDebtInt - totalDebtNoInt

    return totalSaved

