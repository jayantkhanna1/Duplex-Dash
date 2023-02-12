from django.shortcuts import render,redirect
from .models import Admin, User, Listing, UserReviews, ListingReviews
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
                userpackage = user.package
                if userpackage is None:
                    return redirect('packages')
                elif userpackage == "Standard":
                    if int(user.ad_count) >= 3:
                        return redirect('packages')
                    else:
                        return render(request, 'submitad.html')
                return redirect('packages')
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

def newlisting(request):
    tag = request.POST['tag']
    title = request.POST['title']
    description = request.POST['description']
    price = request.POST['price']
    city = request.POST['city']
    state = request.POST['state']
    country = request.POST['country']
    category = request.POST['category']
    feature1 = request.POST['feature1']

    if 'feature2' in request.POST:
        feature2 = request.POST['feature2']
    else:
        feature2 = None

    if 'feature3' in request.POST:
        feature3 = request.POST['feature3']
    else:
        feature3 = None

    if 'feature4' in request.POST:
        feature4 = request.POST['feature4']
    else:
        feature4 = None

    if 'feature5' in request.POST:
        feature5 = request.POST['feature5']
    else:
        feature5 = None

    if 'feature6' in request.POST:
        feature6 = request.POST['feature6']
    else:
        feature6 = None

    mainImage = request.FILES['image1']
    if 'image2' in request.FILES:
        image1 = request.FILES['image2']
    else:
        image1 = None

    if 'image3' in request.FILES:
        image2 = request.FILES['image3']
    else:
        image2 = None

    if 'image4' in request.FILES:
        image3 = request.FILES['image4']
    else:
        image3 = None

    if 'image5' in request.FILES:
        image4 = request.FILES['image5']
    else:
        image4 = None

    if 'image6' in request.FILES:
        image5 = request.FILES['image6']
    else:
        image5 = None

    usertoken  = request.session['TheNairobiPrivateToken']
    user = User.objects.get(private_token=usertoken)
    userpackage = user.package
    if userpackage == "Premium":
        featured = True
    else:
        featured = False
    user = User.objects.get(private_token=usertoken)
    user_name = user.username

    # incrementing ad count
    user.ad_count = int(user.ad_count) + 1
    user.save()

    # Creating Listing
    listing = Listing.objects.create(user=user, user_name=user_name, tag=tag, name=title, description=description, price=price, city=city, state=state, country=country, category=category, feature1=feature1, feature2=feature2, feature3=feature3, feature4=feature4, feature5=feature5, feature6=feature6, mainImage=mainImage, image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, featured=featured)
    listing.save()
    url = "/userprofile?userid="+str(user.id)
    return redirect(url)

def packages(request):
    if 'TheNairobiPrivateToken' in request.session:
        private_token = request.session['TheNairobiPrivateToken']
        if User.objects.filter(private_token=private_token).exists():
            user = User.objects.get(private_token=private_token)
            if user.username == "":
                return redirect('onboarding_form')
            else:
                username = user.username.split(" ")[0].capitalize()
                print(username)
                return render(request, 'packages.html',{'user': user, 'username': username,'private_token': private_token})
        else:
            return redirect('login')
    else:
        return redirect('login')

def buynow(request):
    package = request.GET['package']
    if "TheNairobiPrivateToken" in request.session:
        usertoken = request.session['TheNairobiPrivateToken']
        user = User.objects.get(private_token=usertoken)
        user.package = package
        user.save()
        return redirect('home')
    else:
        return redirect('login')

def userprofile(request):
    if "userid" in request.GET:
        userid = request.GET['userid']
        if User.objects.filter(id=userid).exists():
            user = User.objects.get(id=userid)
            username = user.username.split(" ")[0].capitalize()
            listings = Listing.objects.filter(user=user)
            return render(request, 'userprofile.html',{'user': user, 'username': username, 'listings': listings})
        else:
            return redirect('home')
    else:
        return redirect('home')

