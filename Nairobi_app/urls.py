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

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Adding static path


