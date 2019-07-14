from django.urls import path
from django.conf.urls import url
from . import views



urlpatterns = [
  path('', views.index, name='index'),

  # Auth views
  path('signup/', views.signup, name='signup'),
  path('signup-confirm/', views.signup_confirm, name='signup_confirm'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('success', views.success, name="success"),
  path('populate/<podcast_id>', views.populate_hostprofile, name='populate'),
  path('profile_settings/', views.profile_settings, name='profile_settings'),

]
