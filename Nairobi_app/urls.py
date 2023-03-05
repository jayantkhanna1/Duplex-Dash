from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('signup_form', views.signup_form, name='signup_form'),
    path('otp_verify', views.otp_verify, name='otp_verify'),
    path('onboarding_form', views.onboarding_form, name='onboarding_form'),
    path('onboard_user', views.onboard_user, name='onboard_user'),
    path('logout', views.logout, name='logout'),
    path('login_form', views.login_form, name='login_form'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('forgot_password_form', views.forgot_password_form, name='forgot_password_form'),
    path('otp_verify_forgot_password', views.otp_verify_forgot_password, name='otp_verify_forgot_password'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('submitad', views.submitad, name='submitad'),
    path('newlisting', views.newlisting, name='newlisting'),
    path('packages', views.packages, name='packages'),
    path('pricing', views.packages, name='pricing'),
    path('buynow', views.buynow, name='buynow'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('userdashboard', views.userprofile, name='userprofile'),
    path('new_review', views.new_review, name='new_review'),
    path('showlisting', views.showlisting, name='showlisting'),
    path('new_review_listing', views.new_review_listing, name='new_review_listing'),
    path('send_mail_to_seller', views.send_mail_to_seller, name='send_mail_to_seller'),
    path('delete_listing', views.delete_listing, name='delete_listing'),
    path('search_listing', views.search_listing, name='search_listing'),
    path('ipn', views.ipn, name='ipn'),
    path('verify_phone',views.verify_phone,name="verify_phone"),
    path('paymentConfirmation',views.paymentConfirmation,name="paymentConfirmation"),
    path('contact',views.contact,name="contact"),
    path('contact_admin',views.contact_admin,name="contact_admin"),
    path('usersettings',views.usersettings,name="usersettings"),
    path('change_user_info',views.change_user_info,name="change_user_info"),
    path('admin_login',views.admin_login,name="admin_login"),
    path('admin_login_form',views.admin_login_form,name="admin_login_form"),
    path('admin_logout',views.admin_logout,name="admin_logout"),
    path('admin',views.admin,name="admin"),
    path('add_360_link',views.add_360_link,name="add_360_link"),
    path('make_listing_active',views.make_listing_active,name="make_listing_active"),
    path('make_listing_deactive',views.make_listing_deactive,name="make_listing_deactive"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Adding static path


