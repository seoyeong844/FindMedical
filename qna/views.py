from django.shortcuts import render, get_object_or_404, redirect
from .models import Qna #Community에서의 데이터를 가져오기 위해 --> community.html에서 사용될 듯
from .forms import PostForm
from django.db.models import Q
from django.core.paginator import Paginator
from user.models import Users
from datetime import date, datetime, timedelta

# Create your views here.
def qna(request):
    login_session = request.session.get('login_session', '')
    q = Qna.objects.order_by('-id')
    q_list = Qna.objects.all().order_by('-id')
    paginator = Paginator(q_list,5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'qna.html',{'quiz':q, 'posts':posts, 'login_session':login_session})

def newt(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'newt.html', context)

def postcreatet(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            writer = Users.objects.get(user_id=login_session)
            board = Qna(
                title=form.title,
                body=form.body,
                writer=writer
            )
            board.save()
            return redirect('qna')
        else:
            context['forms'] = form
            if form.errors:
                for value in form.errors.values():
                    context['error'] = value
            return render(request, 'newt.html', context)
    else:
        form = PostForm()
        context['forms'] = form
        return render(request, 'newt.html', context)

def editt(request):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }
    return render(request, 'editt.html', context)

def postupdatet(request, qna_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}
    post = get_object_or_404(Qna, pk=qna_id)
    context['post'] = post
    if post.writer.user_id != login_session:
        return redirect('writet')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.title = form.title
            post.body = form.body
            post.save()
            return redirect('qna')
        else:
            context['forms'] = form
            if form.errors:
                for value in form.errors.values():
                    context['error'] = value
            return render(request, 'editt.html', context)
    elif request.method == 'GET':
        form = PostForm(instance=post)
        context['forms'] = form
        return render(request, 'editt.html', context)

def postdeletet(request, qna_id):
    login_session = request.session.get('login_session', '')
    post = get_object_or_404(Qna, pk=qna_id)
    if post.writer.user_id == login_session:
        post.delete()
        return redirect('qna')
    else:
        return redirect('writet')

def writet(request, qna_id):
    login_session = request.session.get('login_session', '')
    context = { 'login_session' : login_session }

    qna_detail = get_object_or_404(Qna, pk=qna_id)
    context['qna'] = qna_detail

    if qna_detail.writer.user_id == login_session:
        context['writer'] = True
    else:
        context['writer'] = False 
    
    response = render(request, 'writet.html', context)

    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('hitboard3', '_')

    if f'_{qna_id}_' not in cookie_value:
        cookie_value += f'{qna_id}_'
        response.set_cookie('hitboard3', value=cookie_value, max_age=max_age, httponly=True)
        qna_detail.hits += 1
        qna_detail.save()
    return response

def postsearches(request):
    blogs = Qna.objects.all().order_by('-id')

    q = request.POST.get('q', "") 
    title_q = Q(title__icontains = q)
    body_q = Q(body__icontains = q)
    
    if q:
        blogs = blogs.filter(title_q | body_q)
        return render(request, 'postsearches.html', {'blogs' : blogs, 'q' : q})
    
    else:
        return render(request, 'postsearches.html')