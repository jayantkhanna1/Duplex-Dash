from django.contrib import admin
from . models import Admin, User, Listing, UserReviews, ListingReviews

admin.site.register(Admin)
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(UserReviews)
admin.site.register(ListingReviews)
