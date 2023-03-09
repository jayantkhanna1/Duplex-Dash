from django.shortcuts import render,redirect
from .models import Admin, User, Listing, UserReviews, ListingReviews
import random
from django.core.mail import send_mail
from passlib.hash import sha512_crypt as sha512
import os
from django.contrib import messages
import string 
import requests
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()
from django.http import HttpResponse

otp : int
# Create your views here.
def index(request):
    # Getting random listings
    listings = Listing.objects.filter(active = True).order_by('?')[:8]
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

    # Redirecting to OTP page with all information for verification 
    return render(request, 'otp.html',{'email': email,'password': password,'otp': temp_otp})

def otp_verify(request):
    email = request.POST['email']
    password = request.POST['password']
    otp_entered = request.POST['otp']
    otp_built = request.POST['otp_built']

    if otp_entered == str(otp_built):
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

        messages.info(request, 'OTP has been sent to your Email!')
        # Redirecting to OTP page with all information for verification 
        return render(request, 'otp_forgot_password.html',{'email': email,'otp': temp_otp})
    except:
        messages.info(request, 'User Does Not Exist!')
        return redirect('forgot_password')

def otp_verify_forgot_password(request):
    email = request.POST['email']
    otp_entered = request.POST['otp']
    otp_built = request.POST['otp_built']
    if otp_entered == str(otp_built):
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
                return render(request, 'submitad.html')
        else:
            return redirect('login')
    else:
        return redirect('login')
    
def onboard_user(request):
    if "TheNairobiPrivateToken" in request.session:
        username = request.POST['username']
        phone = request.POST['phone']
        extension = request.POST['extension']
        # Twilio phone verify then save
        account_sid = os.getenv('TWILIO_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        otp = random.randint(100000,999999)
        message = client.messages.create(
            body='Hello here is your OTP for Nairobi Listing '+str(otp),
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to="+"+str(extension)+str(phone)
        )
        # Message sent now show OTP page and store all other data in session storage temporarily
        request.session['username'] = username
        request.session['phone'] = "+"+str(extension)+str(phone)
        if 'userimage' in request.FILES:
            image = request.FILES['userimage']
        else:
            image = ""

        if 'redirect' in request.POST:
            request.session['redirect'] = request.POST['redirect']
        else:
            request.session['redirect'] = ""

        if "facebook" in request.POST:
            request.session['facebook'] = request.POST['facebook']
        else:
            request.session['facebook'] = ""
        
        if "twitter" in request.POST:
            request.session['twitter'] = request.POST['twitter']
        else:
            request.session['twitter'] = ""

        if "instagram" in request.POST:
            request.session['instagram'] = request.POST['instagram']
        else:
            request.session['instagram'] = ""

        if "description" in request.POST:
            request.session['description'] = request.POST['description']
        else:
            request.session['description'] = ""

        request.session['otp'] = otp
        return render(request, 'phone_verification.html',{'image':image})
    else:
        return redirect('login')

def verify_phone(request):
    try:
        otp_user = request.POST["otp"]
        otp_got = request.session['otp']
        if str(otp_got) == str(otp_user):
            username = request.session["username"]
            phone = request.session["phone"]
            image = request.POST['image']
            redirect_to = request.session["redirect"]
            private_token = request.session["TheNairobiPrivateToken"]
            description = request.session["description"]
            facebook = request.session["facebook"]
            twitter = request.session["twitter"]
            instagram = request.session["instagram"]
            user = User.objects.get(private_token=private_token)
            user.username = username
            user.phone = phone
            user.image = image
            user.description = description
            user.facebook = facebook
            user.twitter = twitter
            user.instagram = instagram
            if image != "":
                user.image = image
            user.save()
            if redirect_to != "":
                return redirect(redirect_to)
            else:
                return redirect('home')
        else:
            messages.info(request, 'OTP is incorrect!')
            return render(request, 'phone_verification.html')
    except:
        return redirect('home')

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
    if 'location' in request.POST:
        location = request.POST['location']
        if location != "":
            location = location.split("src=")[1]
            location = location.split(" width")[0]
            location = location.replace('"', '') 
    else:
        location = None
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
    listing = Listing.objects.create(user=user, user_name=user_name, tag=tag, name=title, description=description, price=price, city=city, state=state, country=country, category=category, feature1=feature1, feature2=feature2, feature3=feature3, feature4=feature4, feature5=feature5, feature6=feature6, main_image=mainImage, image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, featured=featured,google_map_link = location)
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
        request.session['TheNairobiPackage'] = package
        price = 0
        if package == "Premium":
            price = int(os.getenv("PREMIUM_LISTING_PRICE"))
        elif package == "Standard":
            price = int(os.getenv("STANDARD_LISTING_PRICE"))
        else:
            price = 0

        # Calling Mpesa API to get access token
        params = {
            "consumer_key" : os.getenv("CONSUMER_KEY"),
            "consumer_secret" : os.getenv("CONSUMER_SECRET"),
        }
        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json"
        }
        mpesa_url_1 = os.getenv("MPESA_URL_1")
        data = requests.post(mpesa_url_1, json=params)
        token = data.json()['token']

        # IPN
        mpesa_url_2 = os.getenv("MPESA_URL_2")
        headers={
            "Authentication": "Bearer " + token,
            "Authorization": "Bearer " + token,
            "Accept" : "application/json",
            "Content-Type" : "application/json"
        }
        params = {
            "url" : os.getenv("BASE_URL")+"ipn",
            "ipn_notification_type":"POST",
            "Authentication": "Bearer " + token,
            "Authorization": "Bearer " + token,
        }
        data = requests.post(mpesa_url_2, json=params, headers=headers)
        ipn_data = data.json()

        # Getting IPN endpoints
        mpesa_url_3 = os.getenv("MPESA_URL_3")
        headers={
            "Authentication": "Bearer " + token,
            "Authorization": "Bearer " + token,
            "Accept" : "application/json", 
            "Content-Type" : "application/json"
        }
        params = {
            "Authentication": "Bearer " + token,
            "Authorization": "Bearer " + token,
        }
        data = requests.get(mpesa_url_3, headers=headers, params=params)

        # Submitting payment request
        mpesa_url_4 = os.getenv("MPESA_URL_4")
        headers={
            "Authentication": "Bearer " + token,
            "Authorization": "Bearer " + token,
            "Accept" : "application/json",
            "Content-Type" : "application/json"
        }
        params = {
            "Authentication": "Bearer " + token,
            "Authorization": "Bearer " + token,
            "id" : random.randint(1, 100000000),
            "currency" : "USD",
            "amount" : str(price),
            "description" : "test",
            "callback_url" : os.getenv("BASE_URL")+"paymentConfirmation",
            "notification_id" : ipn_data['ipn_id'],
            "billing_address" :{
                "email_address": "john.doe@example.com",
                "phone_number": "0723xxxxxx",
                "country_code": "KE",
                "first_name": "John",
                "last_name": "Doe",
                "city": "Nairobi",
                "postal_code": "00100",
                "address_line1": "123 Main Street",
                "address_line2": "Apartment 1"
            }
        }

        data = requests.post(mpesa_url_4, json=params, headers=headers)
        submit_data = data.json()
        return redirect(submit_data['redirect_url'])
    else:
        return redirect('login')

def userprofile(request):
    if "userid" in request.GET:
        userid = request.GET['userid']
        if User.objects.filter(id=userid).exists():
            user = User.objects.get(id=userid)
            logged_in_user = None
            if "TheNairobiPrivateToken" in request.session:
                usertoken = request.session['TheNairobiPrivateToken']
                if User.objects.filter(private_token=usertoken).exists():
                    logged_in_user = User.objects.get(private_token=usertoken)
            is_admin = False
            if logged_in_user != None:
                if logged_in_user.id == user.id:
                    is_admin = True
            username = user.username.split(" ")[0].capitalize()
            listings = Listing.objects.filter(user=user,active=True)
            reviews = UserReviews.objects.filter(user_for=user)
            return render(request, 'userprofile.html',{'user': user, 'username': username, 'listings': listings,'reviews': reviews, 'is_admin': is_admin})
        else:
            return redirect('home')
    else:
        return redirect('home')    

def new_review(request):
    user_for = request.POST['user_for']
    user_by = request.POST['user_by']
    review = request.POST['review']
    rating = request.POST['rating_to_be_sent_back']
    subject = request.POST['subject']
    if User.objects.filter(id=user_for).exists():
        user_for = User.objects.get(id=user_for)
        review = UserReviews.objects.create(user_for=user_for, user_by=user_by, review=review, rating=rating, subject=subject)
        review.save()
        # Updating user_for rating
        user_for_rating = UserReviews.objects.filter(user_for=user_for)
        total_rating = 0
        for rating in user_for_rating:
            total_rating = total_rating + int(rating.rating)
        user_for.rating = total_rating / len(user_for_rating)
        user_for.save()
        url = "/userprofile?userid="+str(user_for.id)
        return redirect(url)
    else:
        return redirect('home')

def showlisting(request):
    if "listing_id" in request.GET:
        listingid = request.GET['listing_id']
        listingid = int(listingid)
        if Listing.objects.filter(id=listingid,active=True).exists():
            listing = Listing.objects.get(id=listingid)
            user = listing.user

            similar_listing = Listing.objects.filter(user=user.id,active = True)
            flag = 0
            if len(similar_listing) > 1:
                similar_listing = similar_listing.exclude(id=listing.id)
                similar_listing = similar_listing[0]
                flag =1

            username = user.username.split(" ")[0].capitalize()
            listingname = listing.name.capitalize()
            reviews = ListingReviews.objects.filter(listing=listing)
            if flag == 0 and len(similar_listing) == 1:
                return render(request, 'showlisting.html',{'user': user, 'username': username, 'listing': listing, 'listingname': listingname, 'similar_listing': listing, 'reviews': reviews})
            return render(request, 'showlisting.html',{'user': user, 'username': username, 'listing': listing, 'listingname': listingname, 'similar_listing': similar_listing, 'reviews': reviews})
        else:
            return redirect('home')
    else:
        return redirect('home')

def new_review_listing(request):
    name = request.POST["name"]
    subject = request.POST["subject"]
    rating = request.POST["rating_to_be_sent_back"]
    review = request.POST["review"]
    listing = request.POST["listing"]
    if Listing.objects.filter(id=listing,active=True).exists():
        listing = Listing.objects.get(id=listing)
        review = ListingReviews.objects.create(listing=listing, user=name, subject=subject, rating=rating, review=review)
        review.save()
        # Updating listing rating
        listing_rating = ListingReviews.objects.filter(listing=listing)
        total_rating = 0
        for rating in listing_rating:
            total_rating = total_rating + int(rating.rating)
        listing.rating = total_rating / len(listing_rating)
        listing.save()
        url = "/showlisting?listing_id="+str(listing.id)
        return redirect(url)
    else:
        return redirect('home')

def send_mail_to_seller(request):
    name = request.POST["name"]
    email = request.POST["email"]
    message = request.POST["message"]
    listingid = request.POST["listingid"]
    sender = os.getenv('EMAIL')
    if Listing.objects.filter(id=listingid,active=True).exists():
        listing = Listing.objects.get(id=listingid)
        user = listing.user
        if User.objects.filter(id=user.id).exists():
            user = User.objects.get(id=user.id)
            reciever = [user.email]
            message = "Name : " + name + "\nEmail : " + email + "\nMessage : " + message
            send_mail("Hey there you have a new enquiry for your listing at The Nairobi Listing",message,sender,recipient_list=reciever)
            url = "/showlisting?listing_id="+str(listing.id)
            messages.info(request, 'done')
            return redirect(url)
        else:
            url = "/showlisting?listing_id="+str(listing.id)
            messages.info(request, 'error')
            return redirect(url)
    else:
        url = "/showlisting?listing_id="+str(listing.id)
        messages.info(request, 'error')
        return redirect(url)

def delete_listing(request):
    # Check if user is admin or not
    print(request.GET)
    if "TheNairobiPrivateToken" in request.session:
        usertoken = request.session['TheNairobiPrivateToken']
        if User.objects.filter(private_token=usertoken).exists():
            user = User.objects.get(private_token=usertoken)
            userid = request.GET['user_id']
            userid = int(userid)
            if User.objects.filter(id=userid).exists():
                    user_listing = User.objects.get(id=userid)
                    if user.id == user_listing.id:
                        if "listing_id" in request.GET:
                            listingid = request.GET['listing_id']
                            listingid = int(listingid)
                            if Listing.objects.filter(id=listingid,active=True).exists():
                                listing = Listing.objects.get(id=listingid)
                                listing.delete()
                                # Decrease user listing count
                                user_ad_count = int(user_listing.ad_count) -1
                                user_listing.ad_count = str(user_ad_count)
                                user_listing.save()
                                return redirect('home')
                            else:
                                return redirect('home')
                        else:
                            return redirect('home')
                    else:
                        return redirect('home')
            else:
                    return redirect('home')
        else:
            return redirect('home')
    else:
        return redirect('home')

def search_listing(request):
    where = request.GET['where']
    what = request.GET['what']
    category = request.GET['category']
    listings = Listing.objects.filter(category__icontains=category,active = True)
    listings = listings | Listing.objects.filter(state__icontains=where,active = True)
    listings = listings | Listing.objects.filter(city__icontains=where,active = True)
    listings = listings | Listing.objects.filter(name__icontains=what,active = True)
    listings = listings | Listing.objects.filter(country__icontains=where,active = True)
    return render(request, 'searchlisting.html', {'listings': listings})

def contact(request):
    if "TheNairobiPrivateToken" in request.session:
        usertoken = request.session['TheNairobiPrivateToken']
        if User.objects.filter(private_token=usertoken).exists():
            user = User.objects.get(private_token=usertoken)
            username = user.username.split(" ")[0].capitalize()
            return render(request, 'contact.html', {'user': user, 'username': username, 'login': True})
        else:
            return render(request, 'contact.html')
    return render(request, 'contact.html')

def contact_admin(request):
    name = request.POST["name"]
    email = request.POST["email"]
    message = request.POST["message"]
    message = "Name : " + name + "\nEmail : " + email + "\nMessage : " + message
    sender = os.getenv('EMAIL')
    reciever = [os.getenv('EMAIL')]
    try:
        send_mail("Hey there you have a new query from a user of Nairobi Listing",message,sender,recipient_list=reciever)
        messages.info(request, 'done')
    except:
        messages.info(request, 'error')
    return redirect('contact')

def usersettings(request):
    if "TheNairobiPrivateToken" in request.session:
        usertoken = request.session['TheNairobiPrivateToken']
        if User.objects.filter(private_token=usertoken).exists():
            user = User.objects.get(private_token=usertoken)
            username = user.username.split(" ")[0].capitalize()
            return render(request, 'usersettings.html', {'user': user, 'username': username})
        else:
            return redirect('home')
    return redirect('home')

def change_user_info(request):
    if "TheNairobiPrivateToken" in request.session:
        usertoken = request.session['TheNairobiPrivateToken']
        if User.objects.filter(private_token=usertoken).exists():
            user = User.objects.get(private_token=usertoken)
            username = user.username.split(" ")[0].capitalize()
            if "username" in request.POST:
                username = request.POST["username"]
                user.username = username
                user.save()
                messages.info(request, 'done')
            if "new_password" in request.POST and "old_password" in request.POST and request.POST["new_password"] != "" and request.POST["old_password"] != "":
                new_password = request.POST["new_password"]
                print(new_password)
                if "old_password" in request.POST:
                    old_password = request.POST["old_password"]
                    old_password = sha512.hash(old_password, rounds=5000,salt="NairobiApp")
                    new_password = sha512.hash(new_password, rounds=5000,salt="NairobiApp") 
                    if old_password == user.password:
                        user.password = new_password
                        messages.info(request, 'done')
                        user.save()
                    else:
                        messages.info(request, 'error')
                else:
                    messages.info(request, 'error')
            if "userimg" in request.FILES:
                user_img = request.FILES["userimg"]
                user.image = user_img
                user.save()
                messages.info(request, 'done')
            if "facebook" in request.POST:
                facebook = request.POST["facebook"]
                user.facebook = facebook
                user.save()
                messages.info(request, 'done')
            if "twitter" in request.POST:
                twitter = request.POST["twitter"]
                user.twitter = twitter
                user.save()
                messages.info(request, 'done')
            if "instagram" in request.POST:
                instagram = request.POST["instagram"]
                user.instagram = instagram
                user.save()
                messages.info(request, 'done')
            if "description" in request.POST:
                description = request.POST["description"]
                user.description = description
                user.save()
                messages.info(request, 'done')
            return redirect('usersettings')
        else:
            return redirect('home') 

def admin_login(request):
    return render(request, 'admin_login.html')

def admin(request):
    if "TheNairobiAdminToken" in request.session:
        admintoken = request.session['TheNairobiAdminToken']
        if Admin.objects.filter(private_token=admintoken).exists():
            admin = Admin.objects.get(private_token=admintoken)
            listings = Listing.objects.all()
            users = User.objects.all()
            user_number = len(users)
            revenue = 0
            for i in users:
                if i.package == "Premium":
                    revenue = revenue + int(os.getenv("PREMIUM_LISTING_PRICE"))
                else:
                    revenue = revenue + int(os.getenv("STANDARD_LISTING_PRICE"))
            return render(request, 'admin.html', {'admin': admin,'listings':listings,'users':users,'user_number':user_number,'revenue':revenue})
        else:
            return redirect('adminlogin')
    return redirect('admin_login')

def admin_login_form(request):
    email = request.POST["email"]
    password = request.POST["password"]
    if Admin.objects.filter(email = email).exists():
        admin = Admin.objects.get(email = email)
        if password == admin.password:
            res = ''.join(random.choices(string.ascii_lowercase +string.digits, k=30))
            request.session['TheNairobiAdminToken'] = res
            admin.private_token = res
            admin.save()
            return redirect('admin')
        else:
            messages.info(request,"error")
            return redirect('admin_login')
    else:
        messages.info(request,"error")
        return redirect('admin_login')
    
def admin_logout(request):
    del request.session['TheNairobiAdminToken']
    return redirect('admin_login')

def add_360_link(request):
    link = request.POST["link"]
    listing_id = request.POST["listing_id"]
    listing = Listing.objects.get(id=listing_id)
    listing.video_360_link = link
    listing.save()
    return HttpResponse("done")

def make_listing_active(request):
    listing_id = request.POST["listing_id"]
    listing = Listing.objects.get(id=listing_id)
    listing.active = True
    listing.save()
    return HttpResponse("done")

def make_listing_deactive(request):
    listing_id = request.POST["listing_id"]
    listing = Listing.objects.get(id=listing_id)
    listing.active = False
    listing.save()
    return HttpResponse("done")

def terms_and_condition(request):
    return render(request, 'term.html')

def privacy_policy(request):
    return render(request, 'privacy.html')

def ipn(request):
    print(request.GET)

def paymentConfirmation(request):
    try:
        package = request.session['TheNairobiPackage']
        usertoken = request.session['TheNairobiPrivateToken']
        user = User.objects.get(private_token=usertoken)
        user.package = package
        user.save()
        messages.info(request, 'done')
        return redirect('home')
    except Exception as e:
        messages.info(request, 'error')
        sender = os.getenv('EMAIL')
        reciever = [os.getenv('EMAIL')]
        user = User.objects.get(private_token=request.session['TheNairobiPrivateToken'])
        message = "Email : " + user.email +" \n error : " + "There was an error with the payment of client : "+e   
        message_to_user = "There was an error with your payment. If you are receiving this message it means we have recieved your error and we will get back to you as soon as possible. In the mean time you can contact us on our email address : "+os.getenv("CONSUMER_EMAIL")
        send_mail("Hey there! we have recieved your error.",message_to_user,sender,recipient_list=reciever)
        send_mail("Hey there you have a ERROR from a user of Nairobi Listing. There was an error with client payment",message,sender,recipient_list=reciever)
        return redirect('home')
    

