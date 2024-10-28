from django.shortcuts import render, redirect
from django.http import JsonResponse
from userauth.models import User, ContactUs
from userauth.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

# from django.conf import settings

# # Create your views here.

# User = settings.AUTH_USER_MODEL


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            newuser = form.save()
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            messages.success(
                request, f"Hey {username}, your account was successfully created."
            )

            newuser = authenticate(username=email, password=password)
            login(request, newuser)
            return redirect("core:index")
    else:
        form = UserRegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "userauth/register.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            
            user = User.objects.get(email=email)

            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "logged In successfully")
                return redirect("core:index")
            else:
                messages.warning(request, "User does not exist, create an account.")
        except:
            messages.warning(request, f"User with {email} does not exist.")

    return render(request, "userauth/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out")
    return redirect("userauth:login")

def contactus(request):
    return render(request, 'userauth/contact.html')

def ajaxcontact(request):

    full_name = request.GET.get('full_name')
    email = request.GET.get('email')
    mobile = request.GET.get('mobile')
    subject = request.GET.get('subject')
    message = request.GET.get('message')

    ContactUs.objects.create(
        full_name = full_name,
        email = email,
        phone = mobile,
        subject = subject,
        message = message
    )

    return JsonResponse({'bool':True})

def account_update(request):
    user_id = request.GET.get('user_id')

    index_user = get_object_or_404(User, id=user_id)


    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    email = request.GET.get('email')
    username = request.GET.get('username')
    bio = request.GET.get('bio')

    # Check for unique email constraint
    if email and User.objects.filter(email=email).exclude(id=index_user.id).exists():
        return JsonResponse({'bool': False, 'error': 'Email is already in use.'})


    # Update user fields
    index_user.first_name = first_name
    index_user.last_name = last_name
    index_user.email = email
    index_user.username = username
    index_user.bio = bio  
    
    index_user.save()


    context = render_to_string("userauth/async/account-update.html", {
        'user': index_user,
        })

    return JsonResponse({'bool':True, 'data': context})

