from django.test import TestCase
from hospital_management_app.models import CustomUser, Patient, Doctor, Department, Appointment
# Create your tests here.

# 创建部门
from hospital_management_app.models import Department


def create_patient(start, num):
    for i in range(num):
        username = 'patient' + str(start + i)
        password = '123456'
        email = 'patient' + str(start + i) + '@qq.com'
        first_name = 'patient' + str(start + i)
        last_name = 'patient' + str(start + i)
        address = 'address' + str(start + i)
        age = 20
        contact_number = 123456789
        user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                              first_name=first_name, last_name=last_name, user_type=2)
        patient = Patient.objects.get(admin=user)
        patient.address = address
        patient.age = age
        patient.contact_number = contact_number
        user.save()
        patient.save()


# 创建医生
from hospital_management_app.models import Doctor


def change_doctors_password_to_123():
    doctors = Doctor.objects.all()
    for doctor in doctors:
        doctor.admin.set_password('123')
        doctor.admin.save()
        doctor.save()


if __name__ == '__main__':
    change_doctors_password_to_123()
