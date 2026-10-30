from django.urls import path
from . import views

app_name = "studentapp"
urlpatterns = [
    path("", views.home, name="home"),
    path("astrologers/", views.astrologers, name="astrologers"),
    path("astrologer/<slug:slug>/", views.profile, name="profile"),
    path("booking/success/", views.booking_success, name="booking_success"),
    path("booking/<slug:slug>/", views.booking, name="booking"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

]