from django.shortcuts import render, get_object_or_404, redirect
from .models import ComHospital #Community에서의 데이터를 가져오기 위해 --> community.html에서 사용될 듯
from .forms import PostForm
from django.core.paginator import Paginator
from django.db.models import Q
from user.models import Users
from datetime import date, datetime, timedelta

# Create your views here.
def comhospital(request):
    login_session = request.session.get('login_session', '')
    q = ComHospital.objects.order_by('-id')
    q_list = ComHospital.objects.all().order_by('-id')
    paginator = Paginator(q_list,5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'comhospital.html',{'quiz':q, 'posts':posts, 'login_session':login_session})

def news(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'news.html', context)

def postcreates(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            writer = Users.objects.get(user_id=login_session)
            board = ComHospital(
                title=form.title,
                body=form.body,
                writer=writer
            )
            board.save()
            return redirect('comhospital')
        else:
            context['forms'] = form
            if form.errors:
                for value in form.errors.values():
                    context['error'] = value
            return render(request, 'news.html', context)
    else:
        form = PostForm()
        context['forms'] = form
        return render(request, 'news.html', context)

def edits(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'edits.html', context)

def postupdates(request, comhospital_id):
    login_session = request.session.get('login_session', '')
    post = get_object_or_404(ComHospital, pk=comhospital_id)
    context = {'login_session':login_session}
    context['post'] = post
    if post.writer.user_id != login_session:
        return redirect('writes')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.title = form.title
            post.body = form.body
            post.save()
            return redirect('comhospital')
        else:
            context['forms'] = form
            if form.errors:
                for value in form.errors.values():
                    context['error'] = value
            return render(request, 'edits.html', context)
    elif request.method == 'GET':
        form = PostForm(instance=post)
        context['forms'] = form
        return render(request, 'edits.html', context)

def postdeletes(request, comhospital_id):
    login_session = request.session.get('login_session', '')
    post = get_object_or_404(ComHospital, pk=comhospital_id)
    if post.writer.user_id == login_session:
        post.delete()
        return redirect('comhospital')
    else:
        return redirect('writes')

def writes(request, comhospital_id):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    comhospital_detail = get_object_or_404(ComHospital, pk=comhospital_id)
    context['comhospital'] = comhospital_detail
    if comhospital_detail.writer.user_id == login_session:
        context['writer'] = True
    else:
        context['writer'] = False 
    response = render(request, 'writes.html', context)

    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('hitboard2', '_')

    if f'_{comhospital_id}_' not in cookie_value:
        cookie_value += f'{comhospital_id}_'
        response.set_cookie('hitboard2', value=cookie_value, max_age=max_age, httponly=True)
        comhospital_detail.hits += 1
        comhospital_detail.save()
    return response

def postsearch(request):
    blogs = ComHospital.objects.all().order_by('-id')

    q = request.POST.get('q', "") 
    title_q = Q(title__icontains = q)
    body_q = Q(body__icontains = q)
    
    if q:
        blogs = blogs.filter(title_q | body_q)
        return render(request, 'postsearch.html', {'blogs' : blogs, 'q' : q})
    
    else:
        return render(request, 'postsearch.html')