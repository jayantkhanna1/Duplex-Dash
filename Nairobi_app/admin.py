from django.contrib import admin
from . models import Admin, User, Category, Package, Listing, UserReviews, ListingReviews

admin.site.register(Admin)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Package)
admin.site.register(Listing)
admin.site.register(UserReviews)
admin.site.register(ListingReviews)