from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def calculator(request):
    return render(request, "calculator.html")
