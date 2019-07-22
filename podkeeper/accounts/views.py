from . mailers import send_confirmation_email, reset_password_email
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import CustomUser
from podcasts.podcast_api import search_by_owner, populate_podcast_object
from podcasts.models import Podcast
from django.contrib.auth.decorators import login_required, user_passes_test
from . decorators import email_confirmed
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.password_validation import validate_password
from . tokens import account_activation_token
from django.db.models import Q
# Create your views here.

def signup_error(request, message=None):
  if message is None:
    message = 'Sorry, something went wrong, please try again.'
  
  messages.add_message(request, messages.ERROR, message)
  return redirect('signup')

def index(request):
  if request.user.is_authenticated:
    return redirect('my_profile')

  return render(request, 'homepage.html')

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
    send_confirmation_email(request, user)
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
      return redirect('index')
    else:
      messages.add_message(request, messages.ERROR, 'Wrong username / password combination.')
      return redirect('login')

  return render(request, 'login.html')



def logout_view(request):
  logout(request)
  return redirect('login')

@user_passes_test(email_confirmed, login_url='/signup-confirm/', redirect_field_name=None)
@login_required(login_url='/login/')
def my_profile(request, profile_tab='host'):
  results = None
  if request.method == "POST":
    results = search_by_owner(request.POST.get('search'))
  return render(request, 'my-profile-page.html', {'profile_tab' : profile_tab, 'results' : results})


@user_passes_test(email_confirmed, login_url='/signup-confirm/', redirect_field_name=None)
@login_required(login_url='/login/')
def view_profile(request,user_id ,profile_tab='host'):
  profile = CustomUser.objects.get(pk=user_id)
  if profile == None:
    return redirect('index')
  return render(request, 'view-profile.html', {'profile_tab' : profile_tab, 'profile' : profile })


@user_passes_test(email_confirmed, login_url='/success/', redirect_field_name=None)
@login_required(login_url='/login/')
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

@user_passes_test(email_confirmed, login_url='/signup-confirm/', redirect_field_name=None)
@login_required(login_url='/login/')
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

def homepage(request):
  return render(request, 'homepage.html')


def activate(request, uidb64, token):
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = CustomUser.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
    user = None

  if user is not None and account_activation_token.check_token(user, token):
    user.email_confirmed = True
    user.save()
    return redirect('profile_settings')
  else:
    messages.add_message(request, messages.ERROR, 'Email address is already in use.')
    return redirect('signup')


def reset_password_step1(request):
  if request.method == "POST":
    try:  
      user = CustomUser.objects.get(email=request.POST.get('email'))

    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
      messages.add_message(request, messages.ERROR, 'Email does not exist in our system.')
      return redirect('start_password_reset')

    reset_password_email(request, user)
    return render(request, 'check_your_inbox.html')

  return render(request, 'email_reset_step_one.html')

def reset_password_step2(request, uidb64, token):
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = CustomUser.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
    user = None

  if user is not None and account_activation_token.check_token(user, token):
    request.session['user_pk'] = user.pk
    return redirect('password_reset_final')
  else:
    messages.add_message(request, messages.ERROR, 'Seems like something went wrong, try again!')
    return redirect('start_password_reset')


def reset_password_step3(request):
  if request.method == "POST":
    password = request.POST.get('password')
    user = CustomUser.objects.get(pk=request.session['user_pk'])

    try: 
      password == request.POST.get('confirmpassword')
    except:
      return password_change_error(request=request, message='Passwords did not match.')

    try: 
      validate_password(password, user=User)
    except:
      return password_change_error(request=request, message='Password did not meet minimum security requirements.')

    user.set_password(password)
    user.save()
    return redirect('login')

  return render(request, 'reset_password_final.html')


def search(request):
  if request.method != 'POST':
    return render(request, 'search.html')

  text = request.POST.get('search', '')
  users = CustomUser.objects.filter(
    Q(first_name__icontains=text) |
    Q(last_name__icontains=text) )
  podcasts = Podcast.objects.filter(
    Q(title__icontains=text) |
    Q(description__icontains=text) )
  
  return render(request, 'search.html', {'users' : users, 'podcasts' : podcasts})