from django.shortcuts import render,redirect
from .models import Admin, User, Package, Listing, UserReviews, ListingReviews
import random
from django.core.mail import send_mail
from passlib.hash import sha512_crypt as sha512
import os
from django.contrib import messages
import string 
from dotenv import load_dotenv
load_dotenv()

otp : int
# Create your views here.
def index(request):
    # Getting random listings
    listings = Listing.objects.all().order_by('?')[:8]
    if 'TheNairobiPrivateToken' in request.session:
        # Getting User details
        try:
            user = User.objects.get(private_token=request.session['TheNairobiPrivateToken'])
            if user.username == "":
                return redirect('onboarding_form')
            # Getting just first name of user
            username = user.username.split(" ")[0].capitalize()
            return render(request, 'index.html', {'privatetoken': request.session['TheNairobiPrivateToken'],'login': True,'listings': listings,'user': user,'username':username})
        except:
            pass
    #user = User.objects.get(email="jayantkhanna3105@gmail.com")
    return render(request, 'index.html',{'login': False,'listings': listings})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def signup_form(request):

    # Getting form data
    email = request.POST['email']
    password = request.POST['password']
    password=sha512.hash(password, rounds=5000,salt="NairobiApp")

    # Checking if Email already exists
    try:
        user = User.objects.get(email=email)
        messages.info(request, 'Email Already Exists!')
        return render(request, 'signup.html')
    except:
        pass

    # Creating OTP to verify Email
    temp_otp = random.randint(100000,999999)

    # Sending User Email
    message = "Your OTP for Nairobi Listing is "+str(temp_otp)
    reciever = [email]
    sender = os.getenv('EMAIL')
    send_mail("OTP for Nairobi Listing",message,sender,recipient_list=reciever)

    # Storing OTP in a global variable
    global otp
    otp = temp_otp

    # Redirecting to OTP page with all information for verification 
    return render(request, 'otp.html',{'email': email,'password': password})

def otp_verify(request):
    email = request.POST['email']
    password = request.POST['password']
    otp_entered = request.POST['otp']

    global otp
    if otp_entered == str(otp):
        # Creating Private Token
        res = ''.join(random.choices(string.ascii_lowercase +string.digits, k=30))

        #Storing Private Token in Session
        request.session['TheNairobiPrivateToken'] = res

        # Creating User
        user = User(private_token=res,email=email,password=password)
        user.save()

        return redirect('onboarding_form')
    else:
        messages.info(request, 'OTP is incorrect!')
        return render(request, 'otp.html',{'email': email,'password': password})

def onboarding_form(request):
    # Check if there is a redirect in get request
    if 'redirect' in request.GET:
        redirect = request.GET['redirect']
        return render(request, 'onboarding.html',{'redirect': redirect})
    return render(request, 'onboarding.html',{'redirect': 'home'})

def logout(request):
    del request.session['TheNairobiPrivateToken']
    return redirect('index')

def login_form(request):
    email = request.POST['email']
    password = request.POST['password']

    # Hashing Password
    password=sha512.hash(password, rounds=5000,salt="NairobiApp")

    # Checking if Email exists
    try:
        user = User.objects.get(email=email)
        if user.password == password:
            if user.username == "":
                return redirect('onboarding_form')
            else:
                # Creating Private Token
                res = ''.join(random.choices(string.ascii_lowercase +string.digits, k=30))

                #Storing Private Token in Session
                request.session['TheNairobiPrivateToken'] = res

                # Updating Private Token
                user.private_token = res
                user.save()
                return redirect('index')
        else:
            messages.info(request, 'Password is incorrect!')
            return redirect('login')
    except:
        messages.info(request, 'User Does Not Exist!')
        return redirect('login')

def forgot_password(request):
    return render(request, 'forgot_password.html')

def forgot_password_form(request):
    email = request.POST['email']

    # Checking if Email exists
    try:
        user = User.objects.get(email=email)

        # Creating OTP to verify Email
        temp_otp = random.randint(100000,999999)

        # Sending User Email
        message = "Your OTP for Nairobi Listing is "+str(temp_otp)
        reciever = [email]
        sender = os.getenv('EMAIL')
        send_mail("OTP for Nairobi Listing",message,sender,recipient_list=reciever)

        # Storing OTP in a global variable
        global otp
        otp = temp_otp

        messages.info(request, 'OTP has been sent to your Email!')
        # Redirecting to OTP page with all information for verification 
        return render(request, 'otp_forgot_password.html',{'email': email})
    except:
        messages.info(request, 'User Does Not Exist!')
        return redirect('forgot_password')

def otp_verify_forgot_password(request):
    email = request.POST['email']
    otp_entered = request.POST['otp']

    global otp
    if otp_entered == str(otp):
        return render(request, 'reset_password.html',{'email': email})
    else:
        messages.info(request, 'OTP is incorrect!')
        return render(request, 'otp_forgot_password.html',{'email': email})

def reset_password(request):
    password = request.POST['password']
    confirm_password  = request.POST['confirm_password']
    email = request.POST['email']

    if password != confirm_password:
        messages.info(request, 'Passwords do not match!')
        return render(request, 'reset_password.html',{'email': email})
    
    # Hashing Password
    password=sha512.hash(password, rounds=5000,salt="NairobiApp")

    # Updating Password
    user = User.objects.get(email=email)
    user.password = password
    user.save()

    # Redirecting to Home
    return redirect('index')

def submitad(request):
    if 'TheNairobiPrivateToken' in request.session:
        private_token = request.session['TheNairobiPrivateToken']
        if User.objects.filter(private_token=private_token).exists():
            user = User.objects.get(private_token=private_token)
            if user.username == "":
                return redirect('onboarding_form?redirect=submitad')
            else:
                return render(request, 'submitad.html')
        else:
            return redirect('login')
    else:
        return redirect('login')
    
def onboard_user(request):
    if "TheNairobiPrivateToken" in request.session:
        username = request.POST['username']
        phone = request.POST['phone']
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = ""

        if 'redirect' in request.POST:
            redirect_to = request.POST['redirect']
        else:
            redirect_to = ""
        private_token = request.session['TheNairobiPrivateToken']
        user = User.objects.get(private_token=private_token)
        user.username = username
        user.phone = phone
        if image != "":
            user.image = image
        user.save()

        if redirect_to != "":
            return redirect(redirect_to)
        else:
            return redirect('home')
    else:
        return redirect('login')