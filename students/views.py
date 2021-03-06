from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .tokens import account_activation_token
from django.contrib.auth.models import User
from students.models import Student
from django.conf import settings



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject, from_email, to = '[ST | Platform] Активируйте свой аккаунт!',\
                                      settings.EMAIL_HOST_USER,\
                                      form.cleaned_data.get('email')
            text_content = render_to_string('acc_active_email_alternative.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            html_content = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return render(request, 'firstregdone.html')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        Students = Student(user=user, first_name=user.first_name, last_name=user.last_name)
        Students.save()
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'regdone.html')
    else:
        return render(request, 'errorregdone.html')

# API


def students_login(request):
    databases = User.objects.all().filter(is_active=1).values('username')
    return HttpResponse(databases, content_type='application/json')