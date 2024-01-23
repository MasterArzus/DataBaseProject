from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Patient"), (3, "Doctor"))
    email = models.EmailField(max_length=255, unique=True, default='')
    man = models.CharField(max_length=255, default="0")
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Department(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    intro = models.TextField(null=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    contact_number = models.BigIntegerField(null=True)
    age = models.IntegerField(null=True)
    address = models.TextField()

    history = models.TextField(null=True)
    test_result = models.TextField(null=True)
    room_id = models.IntegerField(null=True)

    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # is_prescript = models.BooleanField(null=False, default='False')
    # prescription = models.TextField(null=True)


class Doctor(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    contact_number = models.BigIntegerField(null=True)
    age = models.IntegerField(null=True)
    office_number = models.CharField(max_length=255, null=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, default=1)

    profile_pic = models.FileField(upload_to='avatars/', null=True)

    profile_pic = models.FileField(upload_to='avatars', null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Appointment(models.Model):
    patient = models.TextField(Patient)
    doctor = models.TextField(Doctor)
    department = models.TextField(Department)
    create_time = models.DateTimeField(auto_now_add=True)
    register_time = models.TextField()
    is_appointed = models.BooleanField(null=False, default=False)
    prescription = models.TextField(null=True)


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Room(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    room_id = models.IntegerField(null=True)
    nurse = models.TextField(null=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 2:
            Patient.objects.create(admin=instance)
        if instance.user_type == 3:
            Doctor.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # if instance.user_type == 1:
    #     instance.adminhod.save()
    if instance.user_type == '2':
        instance.patient.save()
    if instance.user_type == '3':
        instance.doctor.save()




