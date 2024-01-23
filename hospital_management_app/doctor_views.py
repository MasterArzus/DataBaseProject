from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import EditAppointForm, DonePatientPrescriptionForm
from .models import Patient, CustomUser, Appointment,Doctor, Department
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from hospital_management_system import settings


def doctor_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(admin=user)
    context = {
        "user": user,
        "doctor": doctor
    }
    return render(request, "doctor_templates/home_content.html", context)


def profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user
    }
    return render(request, 'doctor_templates/profile.html', context)


def appointment(request):
    try:
        appointments = Appointment.objects.filter(is_appointed=True, doctor=request.user.username)
    except:
        appointments = False
    patients = Patient.objects.all()

    context = {
        "appointments": appointments,
        "patients": patients
    }
    return render(request, "doctor_templates/appointment.html", context)


# 这里需要将合适的医生信息给导入进来，然后将合适的信息给放入presribe的html文件中
def edit_prescription(request, appoint_id):

    request.session['appoint_id'] = appoint_id

    appoint = Appointment.objects.get(id=appoint_id)
    form = EditAppointForm()
    # Filling the form with Data from Database
    form.fields['patient'].initial = appoint.patient
    form.fields['doctor'].initial = appoint.doctor
    form.fields['create_time'].initial = appoint.create_time
    form.fields['register_time'].initial = appoint.register_time
    form.fields['prescription'].initial = appoint.prescription
    context = {
        "id": appoint_id,
        "username": appoint.patient,
        "form": form
    }
    return render(request, "doctor_templates/edit_prescription.html", context)


def done_prescription(request, appoint_id):
    appoint = Appointment.objects.get(id=appoint_id)
    appoint.is_appointed = False
    appoint.save()
    # form = DonePatientPrescriptionForm()
    return redirect('/appointment')


def edit_prescription_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('edit_prescription')
    else:
        appoint_id = request.session.get('appoint_id')
        if appoint_id is None:
            return redirect('/prescription')

        form = EditAppointForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            doctor = form.cleaned_data['doctor']
            create_time = form.cleaned_data['create_time']
            register_time = form.cleaned_data['register_time']
            prescription = form.cleaned_data['prescription']

            try:
                appoint = Appointment.objects.get(id=appoint_id)
                appoint.patient = patient
                appoint.doctor = doctor
                appoint.register_time = register_time
                appoint.create_time = create_time
                appoint.prescription = prescription
                appoint.save()
                del request.session['appoint_id']

                messages.success(request, "Appointment Updated Successfully!")
                return redirect('/appointment')
            except:
                messages.success(request, "Failed to Update.")
                return redirect('/appointment')
        else:
            return redirect('/appointment')


