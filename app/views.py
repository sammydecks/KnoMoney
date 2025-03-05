from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json
from .calculation import calculateResults
from django.views.decorators.csrf import csrf_protect


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
            return JsonResponse({"Error:", err}, status=500)