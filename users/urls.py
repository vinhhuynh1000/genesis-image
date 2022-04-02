from unicodedata import name
from django.urls import path, include
from .views import home, signup, profile, activate, ResetPasswordView, dashboard
from users.views import CustomLoginView
from users.forms import LoginForm
from django.conf.urls import url
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name='home'),
    path('register/', signup, name='register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    path('dashboard/', dashboard ,name='dashboard')
]
