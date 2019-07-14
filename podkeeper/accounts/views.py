
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import CustomUser
from podcasts.podcast_api import search_by_owner, populate_podcast_object
from podcasts.models import Podcast
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
      validate_password(password, user=CustomUser)
    except:
      return signup_error(request=request, message='Password did not meet minimum security requirements.')

    # username validation
    username = request.POST.get('email')
    if CustomUser.objects.filter(username=username).exists():
      return signup_error(request=request, message='This email address is already taken.')

    # name validation
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    if len(first_name) == 0:
      return signup_error(request=request, message='Please enter a first name.')
    if len(last_name) == 0:
      return signup_error(request=request, message='Please enter a last name.')

    # user member creation
    user = CustomUser.objects.create_user(
      first_name=first_name,
      last_name=last_name,
      username=username,
      email=username,
      password=password
    )
    user.save()
    if authenticate(username=username, password=password) is None:
      return signup_error(request=request)

    
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    # send_confirmation_email(request, user)
    return redirect('profile_settings')


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

def success(request, profile_tab='host'):
  results = None
  if request.method == "POST":
    results = search_by_owner(request.POST.get('search'))
  return render(request, 'profile-page.html', {'profile_tab' : profile_tab, 'results' : results})


def populate_hostprofile(request, podcast_id):
  hostprofile = request.user.hostprofile
  if request.user.hostprofile.podcast_set.first() == None: 
    podcast = Podcast.objects.create(host=request.user.hostprofile)
    podcast.save()
  hostprofile.signedup = True
  hostprofile.save()
  populate_podcast_object(listennotes_id = podcast_id, hostprofile=request.user.hostprofile)
  return redirect('success')


def password_change_error(request, message=None):
  if message is None:
    message = 'Sorry, something went wrong, please try again.'
  
  messages.add_message(request, messages.ERROR, message)
  return redirect('password_reset_final')

def profile_settings(request):
  if request.method == "POST":
    user = request.user

    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.company_name = request.POST.get('company_name')
    user.website = request.POST.get('website')
    user.title = request.POST.get('title')
    user.save()
    hostprofile = user.hostprofile 
    hostprofile.ideal_guest_desc = request.POST.get('ideal_guest_desc')
    hostprofile.save()
    password = request.POST.get('password')
    new_password = request.POST.get('new_password')
    if password is '' and new_password is '':
      return redirect('success')
    user = authenticate(request, username=user.username, password=password)
    if user is not None:
      try: 
        validate_password(new_password, user=User)
      except:
        message = 'Password did not meet minimum security requirements.'
        messages.add_message(request, messages.ERROR, message)
        return redirect('profile_settings')
      user.set_password(new_password)
      user.save()
      message = 'Password changed successfully. Please log back in'
      messages.add_message(request, messages.SUCCESS, message)
      return redirect('login')
    elif user is None and password is not None and new_password is not None:
      message = 'Incorrect password.'
      messages.add_message(request, messages.SUCCESS, message)
  return render(request, 'profile_settings_page.html')