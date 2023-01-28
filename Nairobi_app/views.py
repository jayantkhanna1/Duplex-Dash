from django.shortcuts import render,redirect
from .models import Admin, User, Category, Package, Listing, UserReviews, ListingReviews

# Create your views here.
def index(request):
    # Getting random listings
    listings = Listing.objects.all().order_by('?')[:8]

    if 'TheNairobiPrivateToken' in request.session:
        # Getting User details
        user = User.objects.get(username=request.session['TheNairobiPrivateToken'])
        public_token = user.public_token
        return render(request, 'index.html', {'privatetoken': request.session['TheNairobiPrivateToken'],'login': True,'listings': listings,'user': user,'public_token': public_token})
    user = User.objects.get(email="jayantkhanna3105@gmail.com")
    return render(request, 'index.html',{'login': True,'listings': listings})