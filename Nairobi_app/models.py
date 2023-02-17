from django.db import models

# Create your models here.
class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    private_token = models.CharField(max_length=100)

class UserPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    features = models.CharField(max_length=1000)

class User(models.Model):
    username = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    password = models.CharField(max_length=100)
    ad_count = models.CharField(max_length=100,default="0")
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    package = models.CharField(max_length=100,blank=True,null=True)
    rating = models.CharField(max_length=100,default="0")
    image = models.ImageField(upload_to='static/user_images/', default='static/user_images/default_img.jpg')
    private_token = models.CharField(max_length=100)
    facebook = models.CharField(max_length=100,blank=True,null=True)
    twitter = models.CharField(max_length=100,blank=True,null=True)
    instagram = models.CharField(max_length=100,blank=True,null=True)

class Listing(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    price = models.CharField(max_length=100)
    featured = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='static/listing_images/')
    image1 = models.ImageField(upload_to='static/listing_images/',blank=True,null=True)
    image2 = models.ImageField(upload_to='static/listing_images/',blank=True,null=True)
    image3 = models.ImageField(upload_to='static/listing_images/',blank=True,null=True)
    image4 = models.ImageField(upload_to='static/listing_images/',blank=True,null=True)
    image5 = models.ImageField(upload_to='static/listing_images/',blank=True,null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,default="pending")
    feature1 = models.CharField(max_length=100,blank=True,null=True)
    feature2 = models.CharField(max_length=100,blank=True,null=True)
    feature3 = models.CharField(max_length=100,blank=True,null=True)
    feature4 = models.CharField(max_length=100,blank=True,null=True)
    feature5 = models.CharField(max_length=100,blank=True,null=True)
    feature6 = models.CharField(max_length=100,blank=True,null=True)
    rating = models.CharField(max_length=100,default="1")
    video_360_link = models.CharField(max_length=1000,blank=True,null=True)
    google_map_link = models.CharField(max_length=10000,blank=True,null=True)


class UserReviews(models.Model):
    user_for = models.ForeignKey(User, on_delete=models.CASCADE)
    user_by = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    review = models.CharField(max_length=10000)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=100)

class ListingReviews(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    review = models.CharField(max_length=10000)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=100)