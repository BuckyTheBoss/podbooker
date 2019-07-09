
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import User
# Create your views here.

def signup_error(request, message=None):
  if message is None:
    message = 'Sorry, something went wrong, please try again.'
  
  messages.add_message(request, messages.ERROR, message)
  return redirect('signup')

def index(request):
  if request.user.is_authenticated:
    return redirect('dashboard')

  return redirect('login')

def signup(request):
  if request.method == 'POST':
    # privacy policy validation
    if request.POST.get('privacy_policy') is None:
      return signup_error(request=request, message='You must agree to our privacy policy.')

    # password validation
    password = request.POST.get('password')
    try: 
      validate_password(password, user=User)
    except:
      return signup_error(request=request, message='Password did not meet minimum security requirements.')

    # username validation
    username = request.POST.get('email')
    if User.objects.filter(username=username).exists():
      return signup_error(request=request, message='This email address is already taken.')

    # name validation
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    if len(first_name) == 0:
      return signup_error(request=request, message='Please enter a first name.')
    if len(last_name) == 0:
      return signup_error(request=request, message='Please enter a last name.')

    # user member creation
    user = User.objects.create_user(
      first_name=first_name,
      last_name=last_name,
      username=username,
      email=username,
      password=password
    )

    if authenticate(username=username, password=password) is None:
      return signup_error(request=request)


    login(request, user)
    # send_confirmation_email(request, user)
    return redirect('signup_confirm')


  return render(request, 'signup.html')


@login_required(login_url='/login/')
def signup_confirm(request):
  return render(request, 'signup-confirm-email.html')



def login_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('success')
    else:
      messages.add_message(request, messages.ERROR, 'Wrong username / password combination.')
      return redirect('login')

  return render(request, 'login.html')



def logout_view(request):
  logout(request)
  return redirect('login')

def success(request):
	return render(request, 'login_success.html')
