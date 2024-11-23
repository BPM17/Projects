"""
URL configuration for Kabeldi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from kabeldi_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("header", views.Menu, name="menu"),
    path("footer", views.Footer, name="footer"),
    path("", views.index, name="index"),
    path("development", views.Development, name="development"),
    path("infrastructure", views.Infrastructure, name="infrastructure"),
    path("contact", views.Contact, name="contact"),
    path("privacyNotice", views.PrivacyNotice, name="privacyNotice"),
    path("merchandise", views.Merchandise, name="merchandise"),
]
