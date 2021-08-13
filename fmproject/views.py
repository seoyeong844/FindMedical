
from django.shortcuts import render
from user.models import Users

def hello(request):
    
    login_session = request.session.get('login_session', '')
    context = {}

    if login_session == '':
        context['login_session'] = False
    else:
        context['login_session'] = True
    return render(request, 'home.html', context)
