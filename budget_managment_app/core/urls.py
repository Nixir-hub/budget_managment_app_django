"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    # Aplikacje własne
    path('accounts/', include('accounts.urls')),        # rejestracja, edycja, usunięcie konta
    path('categories/', include('categories.urls')),    # CRUD kategorii
    path('budget/', include('budget.urls')),      # CRUD transakcji + summary
    path('', IndexView.as_view(), name='home'),
    # Logowanie, wylogowanie, reset hasła (z `django.contrib.auth`)
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]