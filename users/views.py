
from re import T
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
def home(request):
    return render(request, 'users/home.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            
            return render(request, 'users/home.html', messages.success(request, f'Account created for you. Please confirm your email address to complete the registration '))
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):  
    User = get_user_model()
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return render(request, 'users/thank_you_activation.html')
    else:  
        return HttpResponse('Activation link is invalid!')  
#----------------------------------------------------------------
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


@login_required
def profile(request):
    if request.method == 'POST' and 'submit-profile' in request.POST:
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    



    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def dashboard(request):
    
    return render(request, 'users/dashboard.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')
