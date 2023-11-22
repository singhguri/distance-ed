from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("myappF23/"), name="redirect_to_myapp"),
    path("admin/", admin.site.urls),
    path("myappF23/", include("myappF23.urls")),
]
