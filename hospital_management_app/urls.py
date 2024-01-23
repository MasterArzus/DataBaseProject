"""
Author: Johnson
Time：2023-10-10 4:21
"""
from django.urls import path, include
from . import views, admin_views, patient_views,doctor_views

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('personal_profile', admin_views.personal_profile, name="personal_profile"),
    path('password_change', admin_views.password_change, name="password_change"),
    path('password_change_comfirm', admin_views.password_change_comfirm, name="password_change_comfirm"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('doRegister/', views.doRegister, name="doRegister"),
    # admin的视图函数
    path('admin_home/', admin_views.admin_home, name="admin_home"),
    path('check_email_exist/', admin_views.check_email_exist, name="check_email_exist"),
    path('check_contact_number_exist/', admin_views.check_contact_number_exist, name='check_contact_number_exist'),
    path('check_name_exist/', admin_views.check_name_exist, name='check_name_exist'),
    path('admin_profile/', admin_views.admin_profile, name="admin_profile"),
    path('admin_profile_update/', admin_views.admin_profile_update, name="admin_profile_update"),
    # 关于患者
    path('manage_patient/', admin_views.patient_list_view.as_view(), name='manage_patient'),
    path('add_patient/', admin_views.add_patient, name='add_patient'),
    path('add_patient_save/', admin_views.add_patient_save, name="add_patient_save"),
    path('check_username_exist/', admin_views.check_username_exist, name="check_username_exist"),
    path('delete_patient/<patient_id>/', admin_views.delete_patient, name="delete_patient"),
    path('edit_patient/<patient_id>/', admin_views.edit_patient, name="edit_patient"),
    path('edit_patient_save/', admin_views.edit_patient_save, name="edit_patient_save"),
    path('patient_search/', admin_views.patient_search, name="patient_search"),
    # 关于医生
    path('manage_doctor/', admin_views.manage_doctor, name='manage_doctor'),
    path('add_doctor/', admin_views.add_doctor, name='add_doctor'),
    path('add_doctor_save/', admin_views.add_doctor_save, name="add_doctor_save"),
    path('delete_doctor/<doctor_id>/', admin_views.delete_doctor, name="delete_doctor"),
    path('edit_doctor/<doctor_id>/', admin_views.edit_doctor, name="edit_doctor"),
    path('edit_doctor_save/', admin_views.edit_doctor_save, name="edit_doctor_save"),
    path('doctor_search/', admin_views.doctor_search, name="doctor_search"),
    # 关于部门
    path('manage_department/', admin_views.manage_department, name='manage_department'),
    path('add_department/', admin_views.add_department, name='add_department'),
    path('delete_department/<department_id>/', admin_views.delete_department, name="delete_department"),
    path('edit_department/<department_id>/', admin_views.edit_department, name="edit_department"),
    path('edit_department_save/', admin_views.edit_department_save, name="edit_department_save"),
    path('add_department_save/', admin_views.add_department_save, name="add_department_save"),
    path('view_department/<department_id>/', admin_views.view_department, name="view_department"),
    path('department_search/', admin_views.department_search, name="department_search"),

    # 护士
    path('manage_staff/', admin_views.manage_staff, name='manage_staff'),
    path('add_staff/', admin_views.add_staff, name='add_staff'),
    path('delete_staff/<staff_id>/', admin_views.delete_staff, name="delete_staff"),
    path('add_staff_save/', admin_views.add_staff_save, name="add_staff_save"),

    # 病房
    path('manage_room/', admin_views.manage_room, name='manage_room'),
    path('add_room/', admin_views.add_room, name='add_room'),
    path('add_room_save/', admin_views.add_room_save, name="add_room_save"),
    path('delete_room/<room_id>/', admin_views.delete_room, name="delete_room"),
    path('edit_room/<room_id>/', admin_views.edit_room, name="edit_room"),
    path('edit_room_save/', admin_views.edit_room_save, name="edit_room_save"),

    # 患者页
    path('patient_home/', patient_views.patient_home, name="patient_home"),
    path('patient/personal_profile/', patient_views.patient_profile, name="patient_profile"),
    path('patient/password_change/', patient_views.patient_password_change, name="patient_password_change"),
    path('patient/edit_patient_profile/', patient_views.edit_patient_profile, name="edit_patient_profile"),
    path('patient/edit_patient_profile_save', patient_views.edit_patient_profile_save, name="edit_patient_profile_save"),
    path('patient/register/', patient_views.patient_register, name="patient_register"),
    path('patient/register_save/', patient_views.patient_register_save, name="patient_register_save"),
    path('patient/get_doctor/', patient_views.get_doctor, name="get_doctor"),
    path('patient/show_department', patient_views.show_department, name="show_department"),
    path('patient/detailed_department/<department_id>/', patient_views.detailed_department, name="detailed_department"),
    #
    #
    path('doctor_home/', doctor_views.doctor_home, name="doctor_home"),
    path('profile/', doctor_views.profile, name="profile"),
    path('appointment/', doctor_views.appointment, name="appointment"),
    path('edit_prescription/<appoint_id>/', doctor_views.edit_prescription, name="edit_prescription"),
    path('edit_prescription_save/', doctor_views.edit_prescription_save, name="edit_prescription_save"),
    path('done_prescription/<appoint_id>/', doctor_views.done_prescription, name="done_prescription"),

]
