"""
Author: CL
Time：2023-10-16 22:50
"""
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import EditDoctorForm
from .models import Patient, CustomUser, Doctor, Department, Appointment
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from hospital_management_system import settings


def patient_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    patient = Patient.objects.get(admin=request.user.id)
    try:
        register = Appointment.objects.filter(is_appointed=True, patient=user.username)
    except:
        register = False
    department = Department.objects.all()
    context = {
        "user": user,
        "patient": patient,
        "register": register,
        "department": department
    }
    return render(request, "patient_templates/home_content.html", context)


def patient_profile(request):
    # one from user table
    # another from patient table
    user = CustomUser.objects.get(id=request.user.id)
    patient = Patient.objects.get(admin=request.user.id)
    context = {
        "user": user,
        "patient": patient
    }
    return render(request, 'patient_templates/patient_profile.html', context)


def patient_password_change(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user
    }
    return render(request, 'patient_templates/patient_password_change.html', context)


def patient_password_change_comfirm(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('password_change')
    else:
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = CustomUser.objects.get(id=request.user.id)
        if user.check_password(password):
            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, "Password Changed Successfully")
                return redirect('password_change')
            else:
                messages.error(request, "Password Mismatch")
                return redirect('password_change')
        else:
            messages.error(request, "Wrong Password")
            return redirect('password_change')


# edit page
def edit_patient_profile(request):
    patient = Patient.objects.get(admin=request.user.id)
    context = {
        "patient": patient,
    }
    return render(request, "patient_templates/edit_patient_profile.html", context)

def edit_patient_profile_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('edit_patient_profile')
    else:
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        address = request.POST.get('address')
        age = request.POST.get('age')
        try:

            user = CustomUser.objects.get(email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.patient.address = address
            user.patient.age = age
            user.patient.contact_number = contact_number
            user.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect('patient_profile')
        except Exception as e:
            print(str(e))
            messages.error(request, "Failed to Update Profile!")
            return redirect('edit_patient_profile')


def patient_register(request):
    # one from user table
    # another from patient table
    patient = Patient.objects.get(admin=request.user.id)
    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    context = {
        "patient": patient,
        "departments": departments,
        "doctors": doctors
    }
    return render(request, 'patient_templates/register.html', context)


def patient_register_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('patient_register')
    else:
        department_id = request.POST.get('department_select')
        department = Department.objects.get(id=department_id).name
        print(department_id)
        doctor_id = request.POST.get('doctor_select')
        doctor = Doctor.objects.get(id=doctor_id).admin.username
        print(doctor_id)
        time_select = request.POST.get('time_select')
        print(time_select)
        try:
            register = Appointment.objects.create(patient=request.user.username, doctor=doctor,
                                                  department=department, register_time=time_select, is_appointed=True)
            register.save()
            return redirect('patient_home')
        except Exception as e:
            print(str(e))
            messages.error(request, "Failed to Register!")
            return redirect('patient_register')


def patient_get_register(request):
    # one from user table
    # another from patient table
    patient = Patient.objects.get(admin=request.user.id)
    registers = Appointment.objects.get(patient_id=patient.id)
    context = {
        "patient": patient,
        "registers": registers
    }
    return render(request, 'patient_templates/home_content.html', context)


def get_doctor(request):
    if request.method == 'GET':
        department_id = request.GET['depart_id']
        doctors = Doctor.objects.filter(department_id=department_id)
        username_list = []
        doctor_id_list = []
        for doctor in doctors:
            username_list.append(doctor.admin.username)
            doctor_id_list.append(doctor.id)
        print(username_list)
        return JsonResponse({"username_list": username_list, "doctor_id_list": doctor_id_list}, status=200)
    return JsonResponse({"success": False}, status=400)


def show_department(request):
    departments = Department.objects.all()
    context = {
        "departments": departments,
    }
    return render(request, "patient_templates/show_department.html", context)


def detailed_department(request, department_id):
    doctors = Doctor.objects.filter(department_id=department_id)
    department = Department.objects.get(id=department_id)
    context = {
        "doctors": doctors,
        "department": department
    }
    return render(request, "patient_templates/detailed_department.html", context)
