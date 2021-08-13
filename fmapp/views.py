from django.shortcuts import render, get_object_or_404, redirect
from .models import Community #Community에서의 데이터를 가져오기 위해 --> community.html에서 사용될 듯
from .forms import PostForm, SearchForm
from django.core.paginator import Paginator
from django.db.models import Q
from user.models import Users
from datetime import date, datetime, timedelta

def home(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'home.html', context)

# 아래 함수들 다 수정해야함. 목적에 맞게 id를 받는다거나...등등
def search(request):
    form = SearchForm(request.POST or None)
    if request.method =="POST":
        if form.is_valid():
            배 = request.POST.get("배", None)
    return render(request, 'search.html',{"form":form})

def detail(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'detail.html', context) 
    
def community(request):
    login_session = request.session.get('login_session', '')
    q = Community.objects.order_by('-id')
    q_list = Community.objects.all().order_by('-id')
    paginator = Paginator(q_list,5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'community.html', {'quiz':q, 'posts':posts, 'login_session':login_session})

def map(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'map.html', context)

def developers(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'developers.html', context)

#여기서 새로운 함수를 만들면 --> 새로운 페이지를 만들었다는 거니까 --> urls.py에 지정해주기 
def new(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'new.html', context)

def postcreate(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            writer = Users.objects.get(user_id=login_session)
            board = Community(
                title=form.title,
                body=form.body,
                writer=writer
            )
            board.save()
            return redirect('community')
        else:
            context['forms'] = form
            if form.errors:
                for value in form.errors.values():
                    context['error'] = value
            return render(request, 'new.html', context)
    else:
        form = PostForm()
        context['forms'] = form
        return render(request, 'new.html', context)

def edit(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'edit.html', context)

def postupdate(request, community_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}
    post = get_object_or_404(Community, pk=community_id)
    context['post'] = post

    if post.writer.user_id != login_session:
        return redirect('writef')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.title = form.title
            post.body = form.body
            post.save()
            return redirect('community')
        else:
            context['forms'] = form
            if form.errors:
                for value in form.errors.values():
                    context['error'] = value
            return render(request, 'edit.html', context)
    elif request.method == 'GET':
        form = PostForm(instance=post)
        context['forms'] = form
        return render(request, 'edit.html', context)

def writef(request, community_id):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }

    community_detail = get_object_or_404(Community, pk=community_id)
    context['community'] = community_detail

    if community_detail.writer.user_id == login_session:
        context['writer'] = True
    else:
        context['writer'] = False 
        
    response = render(request, 'writef.html', context)

    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('hitboard', '_')

    if f'_{community_id}_' not in cookie_value:
        cookie_value += f'{community_id}_'
        response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
        community_detail.hits += 1
        community_detail.save()
    return response

def postdelete(request, community_id):
    login_session = request.session.get('login_session', '')
    post = get_object_or_404(Community, pk=community_id)
    if post.writer.user_id == login_session:
        post.delete()
        return redirect('community')
    else:
        return redirect('writef')

def result(request):
    if request.method == 'POST':
        selected = request.POST.getlist('나이[]')
        print(selected)
    return redirect('detail')

def post_search(request):
    blogs = Community.objects.all().order_by('-id')

    q = request.POST.get('q', "") 
    title_q = Q(title__icontains = q)
    body_q = Q(body__icontains = q)
    
    if q:
        blogs = blogs.filter(title_q | body_q)
        return render(request, 'post_search.html', {'blogs' : blogs, 'q' : q})
    
    else:
        return render(request, 'post_search.html')