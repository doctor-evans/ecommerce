from django.urls import path
from userauth import views

app_name = "userauth"

urlpatterns = [
    path("sign-up", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("contact-us", views.contactus, name="contact-us"),
    path("ajax-contact", views.ajaxcontact, name="ajax-contact"),
    path("account-update/", views.account_update, name="account-update"),
]
