from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json
from .calculation import calculateResults, calculateWhatIf
from .simplecalc import calculateSimpleResults
from django.views.decorators.csrf import csrf_protect, csrf_exempt
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
        

@csrf_exempt  # Disables CSRF protection for this view
def track_action(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("action")

            # Log or store action
            print(f"User clicked: {action}")  # Replace with DB storage or analytics

            return JsonResponse({"message": f"Tracked {action} click"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
        