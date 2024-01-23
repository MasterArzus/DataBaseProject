"""
Author: Johnson
Time：2023-10-11 12:12
"""
from django import forms
from hospital_management_app import models


class  EditDoctorForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    # username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    # office_number = forms.CharField(label="office_number", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    age = forms.IntegerField(label='Age', widget=forms.TextInput(attrs={"class": "form-control"}))
    contact_number = forms.IntegerField(label='Contact number',
                                        widget=forms.TextInput(attrs={"class": "form-control"}), )
    department = forms.ModelChoiceField(label='Department', queryset=models.Department.objects.all(),
                                        widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))

    class Meta:
        model = models.Doctor


class EditAppointForm(forms.Form):
    patient = forms.CharField(label='Patient', widget=forms.TextInput(attrs={"class": "form-control"}))
    doctor = forms.CharField(label='Doctor',widget=forms.TextInput(attrs={"class": "form-control"}),)
    create_time = forms.DateTimeField(label="Create_time", widget=forms.DateTimeInput(attrs={"class": "form-control"}))
    register_time = forms.DateTimeField(label="Register_time", widget=forms.DateTimeInput(attrs={"class": "form-control"}))
    prescription = forms.CharField(label="Prescription", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = models.Appointment


class EditRoomForm(forms.Form):
    patient = forms.CharField(label='Patient', widget=forms.TextInput(attrs={"class": "form-control"}))
    doctor = forms.CharField(label='Doctor',widget=forms.TextInput(attrs={"class": "form-control"}),)
    create_time = forms.DateTimeField(label="Create_time", widget=forms.DateTimeInput(attrs={"class": "form-control"}))
    register_time = forms.DateTimeField(label="Register_time", widget=forms.DateTimeInput(attrs={"class": "form-control"}))
    prescription = forms.CharField(label="Prescription", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = models.Appointment

class DonePatientPrescriptionForm(forms.Form):
    is_appointed = forms.BooleanField()

    class Meta:
        model = models.Patient
