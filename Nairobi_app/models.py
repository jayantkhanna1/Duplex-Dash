from django.db import models

# Create your models here.
class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    private_token = models.CharField(max_length=100)
    public_token = models.CharField(max_length=100)

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    package = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/user_images/', default='static/user_images/default_img.jpg')
    private_token = models.CharField(max_length=100)
    public_token = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=100) 
    description = models.CharField(max_length=100)

class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.CharField(max_length=100)

class Listing(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    price = models.CharField(max_length=100)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    mainImage = models.ImageField(upload_to='static/listing_images/')
    image1 = models.ImageField(upload_to='static/listing_images/')
    image2 = models.ImageField(upload_to='static/listing_images/')
    image3 = models.ImageField(upload_to='static/listing_images/')
    image4 = models.ImageField(upload_to='static/listing_images/')
    image5 = models.ImageField(upload_to='static/listing_images/')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)
    features = models.CharField(max_length=10000) 
    rating = models.CharField(max_length=100)

class UserReviews(models.Model):
    user_for = models.ForeignKey(User, on_delete=models.CASCADE)
    user_by = models.CharField(max_length=100)
    review = models.CharField(max_length=10000)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=100)

class ListingReviews(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    review = models.CharField(max_length=10000)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=100)