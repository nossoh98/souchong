"""souchong URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from account.views import (
    register_view, 
    home,
    login_view,
    logout_view,
    )
# from chart.views import ChartView

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('chart/',   include('chart.urls', namespace="chart")),
    

    # =================log in & password==========================
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/',register_view, name='register'),
    #password 내장 함수  -> setting 안에 EMAIL_BACKEND 설정 추가 현재는 develop mode이므로 fake email 인증 시스템(console)에 찍힘
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  #내장 template
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),                         #내장 template
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='main/password_reset/password_change_done.html'), 
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='main/password_reset/password_change.html'), 
        name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset/password_reset_done.html'),
     name='password_reset_done'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
    # =================log in & password==========================
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
