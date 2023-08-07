from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Appointment, Contact
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt
import  datetime
from itertools import chain

# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

@login_required(login_url='/login')
def appointment(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['tel']
        checkup = request.POST['checkup']
        date = request.POST['Date']
        appointment1 = Appointment(User=request.user.username, Name=name, Email=email, Number=number, Checkup=checkup,
                                   Date=date)
        appointment1.save()
        messages.success(request, "Your Appointment is Book  ")

        return redirect('/')
    else:
        return render(request, 'appointment.html')


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if User.objects.filter(username=username).exists():
            messages.error(request, "UserName Already Taken ")

            return redirect('/')
        if User.objects.filter(email=email).exists():
            messages.error(request, "UserName With this Email Already Exists ")

            return redirect('/')
        print(username, firstName, lastName, email, pass1, pass2)

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters ")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, "Username must only contain letter and characters  ")
            return redirect('/')

        if len(pass1) < 8:
            messages.error(request, "Password is too small ")
            return redirect('/')

        if pass1 != pass2:
            messages.error(request, "Password does not match ")
            return redirect('/')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstName
        myuser.last_name = lastName
        myuser.save()
        messages.success(request, "Your icoder  account has been successfull created ")
        return redirect('/')
    else:
        return render(request, 'signup.html')


def handleLogout(request):
    logout(request)
    messages.success(request, "You log out Successfully  ")
    return redirect('/')


def handleLogin(request):
    if request.method == 'POST':
        username = request.POST['loginusername']
        password = request.POST['loginpass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "succesfully Logged In ")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password  ")
            return redirect('/')
    else:
        return render(request, 'login.html')


def contact(request):
    if request.method == "POST":

        name = request.POST.get('name', 'default')
        email = request.POST.get('email', 'default')
        phone = request.POST.get('number', 'default')
        conern = request.POST.get('concern', 'default')

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(conern) < 4:
            messages.error(request, "Please fill the form Correctly  ")
        else:
            contact = Contact(Name=name, Number=phone, Email=email, Concern=conern)
            contact.save()
            messages.success(request, "Your form is submitted ")

        return redirect('/')

    return redirect('/')


def getappointment(request):
    a = Appointment.objects.filter(User=request.user.username)
    # a = dt.strptime("10/12/13", "%m/%d/%y")
    # b= dt.strptime("10/15/13", "%m/%d/%y")
    appointment_list = []
    for user in a :
        if datetime.date.today() > user.Date :
            a = Appointment.objects.filter(id=user.id)
            a.delete()
        else:
            print(user.id)
            appointment_list.append(user)

    # appointment_list = list(chain(*appointment_list))
    print(appointment_list)

    return  render(request,'getappoint.html',{'appointments' : appointment_list, 'length' : len(appointment_list)})


def delete(request,id1):
    a = Appointment.objects.filter(id=id1)
    a.delete()
    messages.success(request,"Your Appointment is Cancelled ")
    return redirect('/')

