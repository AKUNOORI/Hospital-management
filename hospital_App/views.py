from django.shortcuts import render, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from .models import Patient, Profile, Doctors, Token, Invoice, Payment ,CustomUser
import random
from .helper import MessageHandler
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

@csrf_exempt
def home(request):
    if request.COOKIES.get('verified') and request.COOKIES.get('verified')!=None:
        return HttpResponse(" verified.")
    else:
        return HttpResponse(" Not verified.")
    
@csrf_exempt
def home_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request,'registration/index.html')

@csrf_exempt
def AppointmentScheduling(request): #Token generator for Patient
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            username = body["username"]
            age = int(body["age"])
            number = int(body["number"])
            adhar = int(body["adhar"]) if "adhar" in body else 0  # Set default value for adhar
            gender = body["gender"]
            disease = body["disease"]
            address = body["address"]
            password = body["password"]
            confirm_password = body["confirm_password"]
            
            if Token.objects.filter(adhar=adhar).exists():
                return JsonResponse({"message":"Already the user is existing"})
            
            if password != confirm_password:
                return render(request, 'registration/patientsignup.html', {'error': 'Passwords do not match'})

            user = Token.objects.create(username=username, age=age, adhar= adhar, number=number, gender=gender, disease=disease, address=address, password=password)
            user.save()   
            doctors = Doctors.objects.filter(specialization=disease).values("doctorName", "specialization", "availableTimeDate", "endTimeDate")
            return render(request, 'registration/doctorsList.html', {'doctors': doctors})  # Redirect to doctors list with doctor data in context
            
        except Exception as ex:
            return JsonResponse({"Error": str(ex)}) 
        
    return render(request,'registration/patientsignup.html')

@csrf_exempt
def PatientLogin(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode("utf-8"))
            username = body["username"]
            password = body["password"]
        
            user = Token.objects.get(username=username, password=password)
            # user = authenticate(request, username=username, password=password)
            if user is not None:

                auth_login(request, user)
                return JsonResponse({"message": "user login successfully"})
    
            # return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
        except Exception as ex:
            return JsonResponse({"Error": str(ex)}) 
        
    # return render(request, 'registration/login.html')

@csrf_exempt
def register(request):
    if request.method=="POST":
        try:
            if User.objects.filter(username__iexact=request.POST['user_name']).exists():
                return HttpResponse("User already exists")

            user=User.objects.create(username=request.POST['user_name'])
            otp=random.randint(1000,9999)
            profile=Profile.objects.create(user=user,phone_number=request.POST['phone_number'],otp=otp)
            if request.POST['methodOtp']=="methodOtpWhatsapp":
                messagehandler=MessageHandler(request.POST['phone_number'],otp).send_otp_via_whatsapp()
            else:
                messagehandler=MessageHandler(request.POST['phone_number'],otp).send_otp_via_message()
            # red=redirect(f'otp/{profile.uid}/')
            # red.set_cookie("can_otp_enter",True,max_age=600)
            # return red  
        except Exception as ex:
            return JsonResponse({"Error": messagehandler})
    return render(request, 'registration/register.html')


@csrf_exempt
def otpVerify(request,uid):   
    if request.method=="POST":
        profile=Profile.objects.get(uid=uid)     
        if request.COOKIES.get('can_otp_enter')!=None:
            if(profile.otp==request.POST['otp']):
                red=redirect("home")
                red.set_cookie('verified',True)
                return red
            return HttpResponse("wrong otp")
        return HttpResponse("10 minutes passed")        
    # return render(request,"registration/otp.html",{'id':uid})  


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            first_name = body['first_name']
            last_name = body['last_name']
            username = body['username']
            email = body['email']
            password = body['password']

            user = User.objects.create_user(username= username, email= email, password= password, first_name= first_name, last_name= last_name)
            user.save()
            #      if body['user_type'] == 'patient':
        #         patient = Patient.objects.create(user=user, address_line1=address_line1, city=city, state=state, pincode=pincode, profile_picture=profile_picture)
        #         patient.save()
        #      elif body['user_type'] == 'doctor':
        #         doctor = Doctor.objects.create(user=user, address_line1=address_line1, city=city, state=state, pincode=pincode, profile_picture=profile_picture)
        #         doctor.save()
            return JsonResponse({"message":"user created successfully"})
        except Exception as ex:
            return JsonResponse({"Error": "Some error occured"})
        
         
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            username = body['username']
            password = body['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # if hasattr(user, 'patient'):
                #     return redirect('patient_dashboard')
                # elif hasattr(user, 'doctor'):
                #     return redirect('doctor_dashboard')
                return JsonResponse({"message": "user login successfully"})
        except Exception as ex:
            return JsonResponse({"Error": "Some error occured"})
        

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        try:
            logout(request)  
            return JsonResponse({"message": "user logged out successfully"})
        except Exception as ex:
            return JsonResponse({"Error": "Logout failed"})

@csrf_exempt
def createPatient(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            name = body["name"]
            mobile = body['mobile']
            medical_issue = body['medical_issue']
            doj = body['doj']
            doe = body['doe']

            try:
                user = CustomUser.objects.get(pk=name)
            except CustomUser.DoesNotExist:
                return JsonResponse({"Error": "Invalid user ID provided"})

            newPatient = Patient.objects.create(name= user, mobile= mobile, medical_issue= medical_issue, doj= doj, doe= doe)
            newPatient.save()
            return JsonResponse({"success":"Patient created successfully"})

        except Exception as ex:
            return JsonResponse({"Error": ex})              

@csrf_exempt
def listOfPatient(request):
    if request.method == 'GET':
        try:
            body = json.loads(request.body.decode("utf-8"))
            doj = body['doj']
            medical_issue= body['medical_issue']
            patientList = Patient.objects.filter(doj=doj, medical_issue=medical_issue).values()
            return JsonResponse({"patientList": list(patientList)})

        except Exception as ex:
            return JsonResponse({"Error": ex})  

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        try:
            subject = request.POST.get("subject", "")
            message = request.POST.get("message", "")
            from_email = request.POST.get("from_email", "") #my mail id
            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, ["admin@example.com"]) #To mail id
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
                return HttpResponseRedirect("/contact/thanks/")
            else:
                # In reality we'd use a form class
                # to get proper validation errors.
                return HttpResponse("Make sure all fields are entered and valid.")
        except Exception as ex:
            return JsonResponse({"Error": ex}) 
        

@csrf_exempt
def doctorsAssociate(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            dr_name = Doctors.objects.get(doctorName = body["doctorName"])
            drName = dr_name.doctorName
            patientDetails = Patient.objects.filter(medical_issue= dr_name.specialization).values()
            return JsonResponse({"patientList": list(patientDetails)})
        
        except Exception as ex:
            return JsonResponse({"Error": ex}) 

@csrf_exempt
def DrList(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            specialization = body["specialization"]

            drList = Doctors.objects.filter(specialization = specialization).values()

            return JsonResponse({"patientList": list(drList)})

        except Exception as ex:
            return JsonResponse({"Error": ex}) 

@csrf_exempt
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'registration/patientclick.html')


@csrf_exempt
def open_payment_app(request):
    # Check if the app name is valid (e.g., 'phonepe' or 'gpay')
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode("utf-8"))
            app_name = body['app_name']
            if app_name not in ['phonepe', 'gpay']:
                return HttpResponseBadRequest("Invalid payment app")

            # Define the custom URL schemes for PhonePe and Google Pay
            app_urls = {
                'phonepe': 'phonepe://pay?amount=100',
                'gpay': 'upi://pay?pa=your-merchant-vpa@xxx&pn=Merchant%20Name&mc=your-merchant-code&tid=your-transaction-id&tr=your-transaction-ref-id&tn=your-transaction-note&am=100&cu=INR',
            }
            # app_urls = {
            #     'phonepe': 'phonepe://',
            #     'gpay': 'upi://pay',
            # }

            # Generate the redirect URL
            app_url = app_urls.get(app_name)
            if app_url:
                return redirect(app_url)
            else:
                return HttpResponseBadRequest("Payment app URL not found")
        
        except Exception as ex:
            return JsonResponse({"Error": ex}) 
        

@csrf_exempt
def generate_invoice(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            patient_id = body[patient_id]
            invoice_number = body[invoice_number]
            date_issued = body[date_issued]
            due_date = body[due_date]
            total_amount = body[total_amount]
            patient = Patient.objects.get(id=patient_id)
            invoice = Invoice.objects.create(patient=patient,invoice_number=invoice_number,date_issued=date_issued,due_date=due_date,total_amount=total_amount)
            invoice.save()

            return invoice

        except Exception as ex:
            return JsonResponse({"Error": ex}) 

@csrf_exempt
def record_payment(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            invoice_id = body[invoice_id]
            amount_paid = body[amount_paid]
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.total_amount -= amount_paid
            if invoice.total_amount <= 0:
                invoice.is_paid = True
            invoice.save()
            payment = Payment.objects.create(invoice=invoice,amount_paid=amount_paid)

            return payment

        except Exception as ex:
            return JsonResponse({"Error": ex}) 
        
@csrf_exempt
def manual_payment(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            invoice_number = body[invoice_number]
            amount_paid = body[amount_paid]
            invoice = Invoice.objects.get(invoice_number=invoice_number)
            invoice.total_amount -= amount_paid
            if invoice.total_amount <= 0:
                invoice.is_paid = True
            invoice.save()
            payment = Payment.objects.create(invoice=invoice,amount_paid=amount_paid)

            return payment
        except Exception as ex:
            return JsonResponse({"Error": ex}) 