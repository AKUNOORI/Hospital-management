from django.urls import path
from . import views


urlpatterns = [
    path('',views.home_view,name=''),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('otp/<str:uid>/', views.otpVerify, name='otp'),


    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),


    path("createPatient/", views.createPatient, name='createPatient'),
    path('listOfPatient/', views.listOfPatient, name='listOfPatient'),


    path('send_email/', views.send_email, name='send_email'),

    path('doctorsAssociate/', views.doctorsAssociate, name='doctorsAssociate'),
    path('DrList/', views.DrList, name='DrList'),


    path('patientclick/', views.AppointmentScheduling, name='AppointmentScheduling'),

    path('PatientLogin/', views.PatientLogin, name='PatientLogin'),

    path('patientclick_view/', views.patientclick_view, name='patientclick_view'),
    path('open_payment_app/', views.open_payment_app, name='open_payment_app'),


    path('generate_invoice/', views.generate_invoice, name='generate_invoice'),
    path('record_payment/', views.record_payment, name='record_payment'),
    path('manual_payment/', views.manual_payment, name='manual_payment'),



]
