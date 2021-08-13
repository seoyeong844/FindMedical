from django.shortcuts import render, redirect
from django.db import transaction
from .models import Users
from argon2 import PasswordHasher
from .forms import RegisterForm, LoginForm

# Create your views here.

# 회원 가입
def signup(request):
    register_form = RegisterForm()
    context = {'forms' : register_form}

    if request.method == 'GET':
        return render(request, 'signup.html', context)

    elif request.method == 'POST':
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            user = Users(
                user_id=registerform.user_id,
                user_pw=registerform.user_pw,
                user_name=registerform.user_name,
                user_email=registerform.user_email
            )
            user.save()
            #login(request, user)
            return redirect("home")
        else:
            context['forms'] = registerform
            if registerform.errors:
                for value in registerform.errors.values():
                    context['error'] = value
        return render(request, 'signup.html', context)

def login(request):
    loginform = LoginForm()
    context = { 'forms' : loginform }

    if request.method == 'GET':
        return render(request, 'login.html', context)

    elif request.method == 'POST':
        loginform = LoginForm(request.POST)
        user_id = request.POST['user_id']
        if loginform.is_valid():
            request.session['login_session'] = loginform.login_session
            request.session.set_expiry(0)
            return redirect('/')
        else:
            context['forms'] = loginform
            if loginform.errors:
                for value in loginform.errors.values():
                    context['error'] = value
        return render(request, 'login.html', context)

# 로그 아웃
def logout(request):
    request.session.flush()
    return redirect('/')


def hello(request):
    context = {}
    login_session = request.session.get('login_session', '')

    if login_session == '':
        context['login_session'] = False
    else:
        context['login_session'] = True
    return render(request, 'home.html', context)