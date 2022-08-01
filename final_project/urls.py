"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from account.views import (registration_view, logout_view, login_view, confirm)
from maqari.views import (index, show_available_classes,show_my_classes,render_available_classes,get_page_count)
from django_email_verification import urls as email_urls

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index,name='index'),
    
    
    path("show_available_classes/<int:page_no>",show_available_classes,name="show_available_classes"),
    path("available_classes",render_available_classes,name="render_available_classes"),
    path("get_page_count",get_page_count,name="get_page_count"),
    path("my_classes",show_my_classes,name="show_my_classes"),
    

    path("register/",registration_view,name="register"),
    path("logout/",logout_view,name="logout"),
    path("login/",login_view,name="login"),
    path("accounts/",include('account.urls')),
    
    # Email verification
    path('email/<str:token>/',confirm),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='auth_registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='auth_registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth_registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "auth_registration/password_reset_confirm.html"),
    name='password_reset_confirm'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth_registration/password_reset_form.html', 
    email_template_name ="auth_registration/password_reset_email.html"), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth_registration/password_reset_complete.html'),
     name='password_reset_complete'),
]
