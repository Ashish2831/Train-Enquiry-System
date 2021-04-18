from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
import json

# Create your views here.
def Home(request):
    return render(request, 'Train/base.html')

def Contact(request):
    return render(request, 'Train/contact.html')

def Register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    emp_register = Registration_Form()
    if request.method == 'POST':
        register = Registration_Form(request.POST)
        if register.is_valid():
            messages.success(request, "Registration Completed Successfully!!")
            register.save()
            return render(request, 'Train/register.html', {'register' : emp_register, 'success' : True})
        else:
            return render(request, 'Train/register.html', {'register' : register, 'errors' : True})
    return render(request, 'Train/register.html', {'register' : emp_register})

def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    emp_login_form = Login_Form()
    if request.method == "POST":
        login_form = Login_Form(request, request.POST)
        if login_form.is_valid():
            uname = login_form.cleaned_data.get('username')
            upass = login_form.cleaned_data.get('password')
            user = authenticate(username=uname, password=upass)
            if user != None:
                login(request, user)
                messages.success(request, "Login")
                return HttpResponseRedirect("/")
            else:
                return render(request, 'Train/login.html', {'login' : login_form})
        else:
            return render(request, 'Train/login.html', {'login' : login_form, 'errors' : True})
    return render(request, 'Train/login.html', {'login' : emp_login_form})

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def Status(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_form = Status_Form()
    if request.method == "POST":
        form = Status_Form(request.POST)
        if form.is_valid():
            number = form.cleaned_data.get("train_number") 
            date = form.cleaned_data.get("date")
            date = str(date)
            date = date.split("-")
            date = "".join(date)

            details = requests.get(f"http://indianrailapi.com/api/v2/livetrainstatus/apikey/f6ee07684c302ddfd87c50db85fb0110/trainnumber/{number}/date/{date}/")
            
            content = details.content
            dict_str = content.decode("utf-8")
            try:
                details = json.loads(dict_str)
            except:
                return HttpResponse("<h1>Service Unavailable</h1>")

            if "Server busy." in details['Message']:
                return HttpResponse("<h1>Server Busy. Try Again After Few Minutes....</h1>")

            return render(request, 'Train/trainstatus.html', {'details' : details})
        else:
            return render(request, 'Train/status.html', {'form' : form})
    return render(request, 'Train/status.html', {'form' : emp_form})

def Enquiry(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_form = Enquiry_Form()
    if request.method == "POST":
        form = Enquiry_Form(request.POST)
        if form.is_valid():
            From = form.cleaned_data.get("from_station")
            To = form.cleaned_data.get("to_station")

            details = requests.get(f"http://indianrailapi.com/api/v2/TrainBetweenStation/apikey/f6ee07684c302ddfd87c50db85fb0110/From/{From}/To/{To}")

            content = details.content
            dict_str = content.decode("utf-8")
            try:
                details = json.loads(dict_str)
            except:
                return HttpResponse("<h1>Service Unavailable</h1>")

            if "Server busy." in details['Message']:
                return HttpResponse("<h1>Server Busy. Try Again After Few Minutes....</h1>")

            return render(request, 'Train/trainenquiry.html', {'form' : form, 'details' : details})
        else:
            return render(request, 'Train/enquiry.html', {'form' : form})
    return render(request, 'Train/enquiry.html', {'form' : emp_form})

def PnrCheck(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_form = Pnr_Form()
    if request.method == "POST":
        form = Pnr_Form(request.POST)
        if form.is_valid():
            pnr = form.cleaned_data.get("pnr")
            details = requests.get(f"http://indianrailapi.com/api/v2/PNRCheck/apikey/f6ee07684c302ddfd87c50db85fb0110/PNRNumber/{pnr}/")

            content = details.content
            dict_str = content.decode("utf-8")
            try:
                details = json.loads(dict_str)
            except:
                return HttpResponse("<h1>Service Unavailable</h1>")

            if "Server busy." in details['Message']:
                return HttpResponse("<h1>Server Busy. Try Again After Few Minutes....</h1>")
                
            return render(request, "Train/trainpnrcheck.html", {'form' : form, 'details' : details})
        else:
            return render(request, "Train/pnrcheck.html", {'form' : form})
    return render(request, "Train/pnrcheck.html", {'form' : emp_form})
