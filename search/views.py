from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .forms import SearchForm
from django.urls import reverse

# 아래 함수들 다 수정해야함. 목적에 맞게 id를 받는다거나...등등
def search(request):
    login_session = request.session.get('login_session', '')
    form = SearchForm(request.POST or None)
    if request.method =="POST":
        if form.is_valid():
            배 = request.POST.get("배", None)
    return render(request, 'search.html',{"form":form, 'login_session':login_session})



def result(request):
    login_session = request.session.get('login_session', '')
    if request.method == 'POST':
        form = SearchForm(request.POST)
        
        age = request.POST.getlist('나이[]')
        brain = request.POST.getlist('머리[]')
        belly = request.POST.getlist('배[]')
        defe = request.POST.getlist('배변[]')
        neck = request.POST.getlist('목[]')
        breast = request.POST.getlist('유방[]')
        etc = request.POST.getlist('기타[]')
        total = [age, brain, belly, defe, neck, breast, etc]

        whole = []

        vater = 'vater'
        thyroid = 'thyroid'
        stomach = 'stomach'
        cervical = 'cervical'
        lung = 'lung'
        
        if form.is_valid():
            i = 0
            while i < len(total):
                j=0
                while j < len(total[i]):
                    whole.append(total[i][j])
                    j += 1
                i += 1
            return render(request, 'both.html', {'whole':whole})
    else:
        form = SearchForm()
        return render(request, 'search.html', {'login_session':login_session})

def cervical(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'cervical.html', context)

def stomach(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'stomach.html', context)
    
def thyroid(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'thyroid.html', context)

def vater(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'vater.html', context)

def lung(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'lung.html', context)

def breast(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'breast.html', context)

def liver(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'liver.html', context)

def both(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'both.html', context)

