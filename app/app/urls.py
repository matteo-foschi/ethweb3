"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from api.views import (
    homePage,
    tokenReward,
    moralis_auth,
    my_profile,
    request_message,
    verify_message,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("", homePage, name="homePage"),
    path("tokenReward", tokenReward, name="tokenReward"),
    path("moralis_auth", moralis_auth, name="moralis_auth"),
    path("request_message", request_message, name="request_message"),
    path("my_profile", my_profile, name="my_profile"),
    path("verify_message", verify_message, name="verify_message"),
    path("logout", moralis_auth, name="moralis_auth_logout"),
]
