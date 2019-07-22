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
  path('my-profile', views.my_profile, name="my_profile"),
  path('populate/<podcast_id>', views.populate_hostprofile, name='populate'),
  path('profile-settings/', views.profile_settings, name='profile_settings'),

    #email activation
  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

  #email password reset
  url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset_password_step2, name='password_reset'),

  path('reset-password', views.reset_password_step1, name='start_password_reset'),
  path('reset-password/final', views.reset_password_step3, name='password_reset_final'),
  path('search', views.search, name='search'),
  path('view-profile/<int:user_id>', views.view_profile, name="view_profile")

]
