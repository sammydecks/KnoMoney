from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json
from .calculation import calculateInterest
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
            total_interest = calculateInterest(gradDate, loans_df)  # Call your function
            return JsonResponse({"totalInterest": total_interest})

        except Exception as err:
            return JsonResponse({"Error:", err}, status=500)