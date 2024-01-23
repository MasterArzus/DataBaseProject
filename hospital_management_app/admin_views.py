from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.generic import ListView

from .forms import EditDoctorForm
from .models import Patient, CustomUser, Doctor, Department, Appointment, Staff, Room
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from hospital_management_system import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def admin_home(request):
    doctor_count = Doctor.objects.all().count()
    patient_count = Patient.objects.all().count()
    appointment_count = Appointment.objects.all().count()
    department_count = Department.objects.all().count()

    departments = Department.objects.all()
    doctors_count_list_in_department = []
    department_name_list = []
    for department in departments:
        doctors_count = Doctor.objects.filter(department=department).count()
        doctors_count_list_in_department.append(doctors_count)
        department_name_list.append(department.name)

    context = {
        "doctor_count": doctor_count,
        "patient_count": patient_count,
        "appointment_count": appointment_count,
        "department_count": department_count,
        "doctors_count_list_in_department": doctors_count_list_in_department,
        "department_name_list": department_name_list
    }
    return render(request, "admin_templates/home_content.html",context)


def personal_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user
    }
    return render(request, 'admin_templates/personal_profile.html', context)


def password_change_comfirm(request):
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


def password_change(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user
    }
    return render(request, 'admin_templates/password_change.html', context)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user": user
    }
    return render(request, 'admin_templates/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        username = request.POST.get('username')

        try:
            user = CustomUser.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            if password != None and password != "":
                user.set_password(password)
            user.save()
            messages.success(request, "Profile Updated Successfully")

            return redirect('admin_home')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_home')


class patient_list_view(ListView):
    model = Patient
    template_name = 'admin_templates/manage_patient_template.html'
    context_object_name = 'patients'
    paginate_by = 10


# 病人
# def manage_patient(request):
#     patients = Patient.objects.all()
#     paginator = Paginator(patients, 7)
#     page = request.GET.get('page')
#
#     try:
#         page_obj = paginator.page(page)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)
#     is_paginated = True if paginator.num_pages > 1 else False # 如果页数小于1不使用分页
#     context = {
#         "page_obj": page_obj,
#         'is_paginated': is_paginated
#     }
#     return render(request, "admin_templates/manage_patient_template.html", context)


def add_patient(request):
    return render(request, "admin_templates/add_patient_template.html")


def add_patient_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_patient')
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        age = request.POST.get('age')
        contact_number = request.POST.get('contact_number')
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  first_name=first_name, last_name=last_name, user_type=2)
            patient = Patient.objects.get(admin=user)
            patient.address = address
            patient.age = age
            patient.contact_number = contact_number
            patient.save()
            user.save()

            messages.success(request, "Patient Added Successfully!")
            return redirect('add_patient')
        except Exception as e:
            print(str(e))
            messages.error(request, "Failed to Add Patient!")
            return redirect('add_patient')


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_contact_number_exist(request):
    contact_number = request.POST.get("contact_number")
    user_obj = Patient.objects.filter(contact_number=contact_number).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        print("YES")
        return HttpResponse(True)
    else:
        print("NO")
        return HttpResponse(False)


def delete_patient(request, patient_id):
    patient = Patient.objects.get(admin=patient_id)
    customuser = CustomUser.objects.get(id=patient_id)
    try:
        patient.delete()
        customuser.delete()
        messages.success(request, "Patient Deleted Successfully!")
        return redirect('manage_patient')
    except:
        messages.error(request, "Failed to Delete Patient!")
        return redirect('manage_patient')


def edit_patient(request, patient_id):
    patient = Patient.objects.get(admin=patient_id)
    context = {
        "patient": patient,
        "id": patient_id
    }
    return render(request, "admin_templates/edit_patient_template.html", context)


def edit_patient_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('edit_patient')
    else:
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        patient_id = request.POST.get('patient_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        address = request.POST.get('address')
        age = request.POST.get('age')

        try:
            print(request)
            user = CustomUser.objects.get(id=patient_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.patient.address = address
            user.patient.age = age
            user.patient.contact_number = contact_number
            user.save()
            messages.success(request, "Patient Updated Successfully!")
            return redirect('manage_patient')
        except Exception as e:
            print(str(e))
            messages.error(request, "Failed to Update Patient!")
            return redirect('manage_patient')


def patient_search(request):
    q_name = request.GET.get('q')
    if q_name:
        match_patient = Patient.objects.filter(admin__first_name__icontains=q_name)
        if match_patient:
            context = {
                "page_obj": match_patient
            }
            return render(request, 'admin_templates/manage_patient_template.html', context)
        match_patient = Patient.objects.filter(admin__last_name__icontains=q_name)
        if match_patient:
            context = {
                "page_obj": match_patient
            }
            return render(request, 'admin_templates/manage_patient_template.html', context)

        messages.error(request, "no result")
        patients = Patient.objects.all()
        context = {
            "page_obj": patients
        }
    messages.error(request, "no result")
    patients = Patient.objects.all()
    context = {
        "page_obj": patients
    }
    return render(request, 'admin_templates/manage_patient_template.html', context)


# 医生
def doctor_search(request):
    q_name = request.GET.get('q')
    if q_name:
        match_doctor = Doctor.objects.filter(admin__first_name__icontains=q_name)
        if match_doctor:
            context = {
                "doctors": match_doctor
            }
            return render(request, 'admin_templates/manage_doctor_template.html', context)
        match_doctor = Doctor.objects.filter(admin__last_name__icontains=q_name)
        if match_doctor:
            context = {
                "doctors": match_doctor
            }
            return render(request, 'admin_templates/manage_doctor_template.html', context)

        messages.error(request, "no result")
        doctors = Doctor.objects.all()
        context = {
            "doctors": doctors
        }
    messages.error(request, "no result")
    doctors = Doctor.objects.all()
    context = {
        "doctors": doctors
    }
    return render(request, 'admin_templates/manage_doctor_template.html', context)


def manage_doctor(request):
    doctors = Doctor.objects.all()
    paginator = Paginator(doctors, 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False # 如果页数小于1不使用分页
    context = {
        "doctors": doctors,
        'page_obj': page_obj,
        'is_paginated': is_paginated
    }
    return render(request, "admin_templates/manage_doctor_template.html", context)


def add_doctor(request):
    form = EditDoctorForm()
    context = {
        "form": form
    }
    return render(request, "admin_templates/add_doctor_template.html", context)



def add_doctor_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_doctor')
    else:
        form = EditDoctorForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            # username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            # office_number = form.cleaned_data['office_number']
            department = form.cleaned_data['department']
            contact_number = form.cleaned_data['contact_number']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage(location=settings.MEDIA_ROOT + '\\avatars',
                                       base_url=settings.MEDIA_URL + 'avatars')
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.create_user(username=first_name + ' ' + last_name, first_name=first_name,
                                                      last_name=last_name, email=email, password='123', user_type=3)
                user.doctor.age = age
                user.doctor.contact_number = contact_number
                user.doctor.department = department

                if profile_pic_url != None:
                    user.doctor.profile_pic = profile_pic_url
                user.save()
                user.doctor.save()
                messages.success(request, "Doctor Added Successfully!")
                return redirect('manage_doctor')
            except Exception as e:
                print(str(e))
                messages.error(request, "Failed to Add Doctor!")
                return redirect('add_doctor')
        return redirect('add_doctor')


def delete_doctor(request, doctor_id):
    doctor = Doctor.objects.get(admin=doctor_id)
    customuser = CustomUser.objects.get(id=doctor_id)
    try:
        doctor.delete()
        customuser.delete()
        messages.success(request, "Doctor Deleted Successfully!")
        return redirect('manage_doctor')
    except:
        messages.error(request, "Failed to Delete Doctor!")
        return redirect('manage_doctor')


def edit_doctor(request, doctor_id):
    request.session['doctor_id'] = doctor_id

    doctor = Doctor.objects.get(admin=doctor_id)
    form = EditDoctorForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = doctor.admin.email
    # form.fields['username'].initial = doctor.admin.username
    form.fields['first_name'].initial = doctor.admin.first_name
    form.fields['last_name'].initial = doctor.admin.last_name
    # form.fields['office_number'].initial = doctor.office_number
    form.fields['age'].initial = doctor.age
    form.fields['department'].initial = doctor.department
    form.fields['contact_number'].initial = doctor.contact_number
    context = {
        "id": doctor_id,
        "username": doctor.admin.username,
        "form": form
    }
    return render(request, "admin_templates/edit_doctor_template.html", context)


def edit_doctor_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('edit_doctor')
    else:
        doctor_id = request.session.get('doctor_id')
        if doctor_id == None:
            return redirect('/manage_doctor')

        form = EditDoctorForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            # username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            # office_number = form.cleaned_data['office_number']
            department = form.cleaned_data['department']
            contact_number = form.cleaned_data['contact_number']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/avatars',
                                       base_url=settings.MEDIA_URL + 'avatars')
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)

            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=doctor_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = first_name + ' ' + last_name
                user.save()

                # Then Update Students Table
                doctor = Doctor.objects.get(admin=doctor_id)
                # doctor.office_number = office_number
                doctor.age = age
                doctor.department = department
                doctor.contact_number = contact_number

                if profile_pic_url != None:
                    doctor.profile_pic = profile_pic_url
                doctor.save()
                # Delete student_id SESSION after the data is updated
                del request.session['doctor_id']

                messages.success(request, "Doctor Updated Successfully!")
                return redirect('manage_doctor')
            except Exception as e:
                print(str(e))
                messages.error(request, "Failed to Update Doctor.")
                return redirect('/edit_doctor/' + doctor_id)
        else:
            return redirect('/edit_doctor/' + doctor_id)


# 关于部门
def department_search(request):
    q_name = request.GET.get('q')
    if q_name:
        match_department = Department.objects.filter(name__icontains=q_name)
        if match_department:
            context = {
                "departments": match_department
            }
            return render(request, 'admin_templates/manage_department_template.html', context)

        messages.error(request, "no result")
        departments = Department.objects.all()
        context = {
            "departments": departments
        }
    messages.error(request, "no result")
    departments = Department.objects.all()
    context = {
        "departments": departments
    }
    return render(request, 'admin_templates/manage_department_template.html', context)


def manage_department(request):
    departments = Department.objects.all()

    context = {
        "departments": departments,

    }
    return render(request, "admin_templates/manage_department_template.html", context)


def add_department(request):
    return render(request, "admin_templates/add_department_template.html")


def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    try:
        department.delete()
        messages.success(request, "Department Deleted Successfully!")
        return redirect('manage_department')
    except:
        messages.error(request, "Failed to Delete Department!")
        return redirect('manage_department')


def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    context = {
        "department": department,
        "id": department_id
    }
    return render(request, "admin_templates/edit_department_template.html", context)


def edit_department_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('edit_department')
    else:
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('name')
        try:
            department = Department.objects.get(id=department_id)
            department.name = department_name
            department.save()
            messages.success(request, "Department Updated Successfully!")
            return redirect('/edit_department/' + department_id)
        except:
            messages.error(request, "Failed to Update Department!")
            return redirect('/edit_department/' + department_id)


def manage_staff(request):
    staffs = Staff.objects.all()
    context = {
        "staffs": staffs,
    }
    return render(request, "admin_templates/manage_staff_template.html", context)


def add_staff(request):
    return render(request, "admin_templates/add_staff_template.html")


def delete_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully!")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Department!")
        return redirect('manage_staff')


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_staff')
    else:
        name = request.POST.get('name')
        if name == "":
            messages.error(request, "The name of nurse cannot be empty!")
            return redirect('add_staff')
        try:
            staff = Staff(name=name)
            staff.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('manage_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('manage_staff')


@csrf_exempt
def check_name_exist(request):
    name = request.POST.get("name")
    department_obj = Department.objects.filter(name=name).exists()
    if department_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def add_department_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_department')
    else:
        name = request.POST.get('name')
        try:
            department = Department(name=name)
            department.save()
            messages.success(request, "Department Added Successfully!")
            return redirect('manage_department')
        except:
            messages.error(request, "Failed to Add Department!")
            return redirect('manage_department')


def view_department(request, department_id):
    doctors = Doctor.objects.filter(department_id=department_id)
    department = Department.objects.get(id=department_id)
    context = {
        "doctors": doctors,
        "department": department
    }
    return render(request, "admin_templates/view_department_template.html", context)


def manage_room(request):
    rooms = Room.objects.all()
    paginator = Paginator(rooms, 5)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页
    context = {
        "rooms": rooms,
        'page_obj': page_obj,
        'is_paginated': is_paginated
    }
    return render(request, "admin_templates/manage_room_template.html", context)


def add_room(request):
    patients = Patient.objects.all()
    context = {
        "patients": patients,
    }
    return render(request, "admin_templates/add_room_template.html", context)


def add_room_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('manage_room')
    else:
        patient_id = request.POST.get('patient_select')
        patient = Patient.objects.get(id=patient_id)
        nurse = request.POST.get('name')
        try:
            room = Room(patient=patient, nurse=nurse)
            room.save()
            messages.success(request, "Room Added Successfully!")
            return redirect('manage_room')
        except Exception as e:
            print(str(e))
            messages.error(request, "Failed to Add Room!")
            return redirect('manage_room')


def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    try:
        room.delete()
        messages.success(request, "Room Deleted Successfully!")
        return redirect('manage_room')
    except:
        messages.error(request, "Failed to Delete Room!")
        return redirect('manage_room')


def edit_room(request, room_id):
    room = Room.objects.get(id=room_id)
    patients = Patient.objects.all()
    context = {
        "patients": patients,
        "room": room
    }
    return render(request, "admin_templates/edit_room_template.html", context)


def edit_room_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_room')
    else:
        patient_id = request.POST.get('patient_select')
        patient = Patient.objects.get(id=patient_id)
        nurse = request.POST.get('name')
        room_id = request.POST.get('room_id')

        try:
            room = Room.objects.get(id=room_id)
            room.patient = patient
            room.nurse = nurse
            room.save()
            messages.success(request, "Room Updated Successfully!")
            return redirect('manage_room')
        except Exception as e:
            print(str(e))
            messages.error(request, "Failed to Update Room!")
            return redirect('manage_room')

