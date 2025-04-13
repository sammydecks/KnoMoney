from django.shortcuts import render
from django.http import JsonResponse
from django.db import models
from .models import EmailList, LoanCalculation, IndividualLoan, SharedEmail, SimpleCalculation
import pandas as pd
import json
from .calculation import calculateResults, calculateWhatIf, getInterestRate, calcSumLoans, calcSumCapLoans
from .simplecalc import calculateSimpleResults
from django.views.decorators.csrf import csrf_protect
# only for TEMP share POST
from enum import Enum

class LoanRangeEnum(Enum):
    range1 = "~ $10K"
    range2 = "~ $20K"
    range3 = "~ $30K"
    range4 = "~ $40K"


# Create your views here.
def home(request):
    return render(request, "home.html")

def calculator(request):
    return render(request, "calculator.html")

def faq(request):
    return render(request, "faq.html")

@csrf_protect
def get_interestrate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from the frontend and turn to Python dictionary
            semester = data["semester"]

            # call initial function of calculating results
            interest = getInterestRate(semester)
            return JsonResponse({"interest": interest})
        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)
    return JsonResponse({"error": "POST only"}, status=405)  # Add this line

@csrf_protect
def calculate_interest(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from the frontend and turn to Python dictionary
            gradDate = pd.to_datetime(data["gradDate"])
            loans_df = pd.DataFrame(data["loans"])  # Convert JSON to pandas DataFrame
            # call initial function of calculating results
            results = calculateResults(gradDate, loans_df)
            return JsonResponse({"totalInterest": results['totalInterest'],
                                 "totalSaved": results['totalSaved'],
                                 "monthlyPay": results['monthlyPay'],
                                 "savedGracePeriod": results['savedGracePeriod'],
                                 "savedAllYears": results['savedAllYears']})

        except Exception as err:
            return JsonResponse({"Error:", err}, safe=False, status=500)


@csrf_protect
def calculate_sum_loans(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from the frontend and turn to Python dictionary
            loans_df = pd.DataFrame(data["loans"])  # Convert JSON to pandas DataFrame
            # call initial function of calculating results
            results = calcSumLoans(loans_df)
            results = f"${results:,}"
            return JsonResponse({"total": results})

        except Exception as err:
            return JsonResponse({"Error:", err}, safe=False, status=500)

@csrf_protect
def calculate_sum_cap_loans(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from the frontend and turn to Python dictionary
            gradDate = pd.to_datetime(data["gradDate"])
            loans_df = pd.DataFrame(data["loans"])  # Convert JSON to pandas DataFrame
            # call initial function of calculating results
            results = calcSumCapLoans(gradDate, loans_df)
            results = f"${results:,}"
            return JsonResponse({"total": results})

        except Exception as err:
            return JsonResponse({"Error:", err}, safe=False, status=500)


@csrf_protect
def calculate_whatif(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from the frontend and turn to Python dictionary
            gradDate = pd.to_datetime(data["gradDate"])
            loans_df = pd.DataFrame(data["loans"])  # Convert JSON to pandas DataFrame
            payment = float(data["customPayment"])

            # call initial function of calculating results
            results = calculateWhatIf(gradDate, loans_df, payment)
            return JsonResponse({"savedGracePeriod": results['savedGracePeriod'],
                                 "savedAllYears": results['savedAllYears'],
                                 "isLargerPayment": results.get('isLargerPayment', False)})

        except Exception as err:
            return JsonResponse({"Error:", err}, safe=False, status=500)

# HOME PAGE CALCULATION SIMPLE SAVINGS    
@csrf_protect
def calculate_savings_simple(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from the frontend and turn to Python dictionary
            gradDate = pd.to_datetime(data["gradDate"])
            loanRange = data["selectedDebtRange"]
            # Convert to Enum
            try:
                loanRangeEnum = LoanRangeEnum(loanRange)  # Get Enum name as a string
            except ValueError:
                loanRangeEnum = "UNKNOWN"

            # call initial function of calculating results
            results = calculateSimpleResults(gradDate, loanRangeEnum)
            results = f"${results:,}" #formatting results
            return JsonResponse({"totalSaved": results})
        
        except Exception as err:
            return JsonResponse({"Error:", err}, safe=False, status=500)

# Save emails to database for mailing list
@csrf_protect
def upload_emaillist(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ref_email = data["email"]

            # Debug print to see what you're getting
            print(f"Received email: {ref_email}")

            # save email to database EmailList table
            EmailList.objects.create(email=ref_email)     

            return JsonResponse({"message": "Email saved successfully!"}) 
        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)
    return JsonResponse({"error": "POST only"}, status=405)  # Add this line

@csrf_protect
def upload_sharedemail(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ref_email = data["email"]

            # Debug print to see what you're getting
            print(f"Received email: {ref_email}")

            # save email to database SharedEmails table
            SharedEmail.objects.create(email=ref_email)     

            return JsonResponse({"message": "Shared email saved successfully!"}) 
        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)
    return JsonResponse({"error": "POST only"}, status=405)  # Add this line

# Save loan calculation to database
@csrf_protect
def upload_calculation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from the frontend and turn to Python dictionary
            grad_date = pd.to_datetime(data["gradDate"])
            loans = data["loans"]

            # loan calculation to loan calculation table
            loan_calc = LoanCalculation.objects.create(expected_grad_date=grad_date)     
            # save each individual loan to individual loan table
            for loan in loans:
                IndividualLoan.objects.create(
                    loancalculation=loan_calc,
                    loan_num=loan["loanNum"],
                    principal=loan["principal"],
                    interest=loan["interest"],
                    loan_type=loan["type"],
                    sem_received=loan["semReceived"]
                )
            return JsonResponse({"message": "Loan calculation saved successfully!"}) 
        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)
    return JsonResponse({"error": "POST only"}, status=405)


# Save simple calculations made
@csrf_protect
def upload_simplecalc(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from the frontend and turn to Python dictionary
            grad_date = pd.to_datetime(data["gradDate"])
            loan_range = data["selectedDebtRange"]

            # save simple calculation to database
            SimpleCalculation.objects.create(
                expected_grad_date=grad_date,
                loan_amount=loan_range
            )     
            return JsonResponse({"message": "Simple calculation saved successfully!"}) 
        except Exception as err:
            return JsonResponse({"error": str(err)}, status=500)
    return JsonResponse({"error": "POST only"}, status=405)