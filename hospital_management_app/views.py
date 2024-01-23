from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from hospital_management_app.EmailBackEnd import EmailBackEnd
from hospital_management_app.models import CustomUser, Patient, Doctor


# Create your views here.
def loginPage(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, email=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')

            elif user_type == '2':
                # return HttpResponse("Patient Login")
                # 进行了重定向
                return redirect("patient_home")

            elif user_type == '3':
                # return HttpResponse("Doctor Login")
                return redirect("doctor_home")
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('login')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: " + request.user.email + " User Type: " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def sign_up(request):
    return render(request, 'sign_up.html')


def doRegister(request):
    if request.method != "POST":
        return HttpResponse("Register Fail!")
    else:
        # Get the post parameters

        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('type')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = first_name + ' ' + last_name
        age = request.POST.get('age')
        # Check for errorneous inputs
        if password1 != password2:
            messages.error(request, "Password do not match")
            return redirect('sign_up')

        # Create the user
        if user_type == '2':
            try:
                user = CustomUser.objects.create_user(username=username, password=password1, email=email,
                                                      first_name=first_name, last_name=last_name,
                                                      user_type=2)
                patient = Patient.objects.get(admin=user)
                patient.contact_number = contact_number
                patient.age = age
                user.save()
                patient.save()
            except Exception as e:
                print(str(e))
                messages.error(request, "Failed to Add Patient!")
                return redirect('login')
        elif user_type == '3':
            try:
                user = CustomUser.objects.create_user(username=username, password=password1, email=email,
                                                      first_name=first_name, last_name=last_name,
                                                      user_type=3)
                doctor = Doctor.objects.get(admin=user)
                doctor.contact_number = contact_number
                doctor.age = age
                user.save()
                doctor.save()
            except Exception as e:
                print(str(e))
                messages.error(request, "Failed to Add Doctor!")
                return redirect('login')

    messages.success(request, "Register successfully!")
    return redirect('login')
