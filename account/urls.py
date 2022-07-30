from django.urls import path
from account.views import resend_email, show_profile

urlpatterns = [
    
    path("resend_email",resend_email,name="resend_email"),
    path("profile/<int:user_id>",show_profile,name="show_profile")
]