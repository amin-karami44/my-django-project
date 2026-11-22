from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
# Create your views here.
from .models import Post,Account,Comment
from .forms import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from django.core.mail import EmailMessage



def index(request):
    posts = Post.published.all()[:3]

    return render(request, 'blog/home.html', {'posts': posts})


def postlist(request):
    posts=Post.published.all()
    paginator=Paginator(posts,2)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    
    return render (request,'blog/post/list.html',{'posts':posts,'page':page})

#class PostList(ListView):
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by= 2
    template_name= 'blog/post/list.html' 


def postdetail(request,slug,pk):
    post=get_object_or_404(Post,status='published',slug=slug,id=pk)
    comments=post.comments.filter(active=True)
    new_comment=None
    if request.method=='POST':
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    else:
        comment_form=CommentForm()
    context={
        'post':post,
        'new_comment':new_comment,
        'comments':comments,
        'comment_form':comment_form
    }        
    return render(request,'blog/post/detail.html',context)



@login_required
def UserAccount(request):
    user = request.user

    account, created = Account.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = AccountForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user.first_name = form.cleaned_data['name']
                user.last_name = form.cleaned_data['last_name']
                user.save()

                account.gender = form.cleaned_data['gender']
                account.address = form.cleaned_data['address']
                account.age = form.cleaned_data['age']
                account.phone = form.cleaned_data['phone']
                account.save()

            return redirect('blog:index')

    else:
        form = AccountForm(initial={
            'name': user.first_name,
            'last_name': user.last_name,
            'phone': account.phone,
            'gender': account.gender,
            'address': account.address,
            'age': account.age,
        })

    return render(
        request,
        'blog/forms/account_form.html',
        {
            'form': form,
            'account': account
        }
    )



def ContactUs(request):
    sent = False

    if request.method == 'POST':
        form = ContactusForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            subject = f"پیام جدید از سایت: {cd['subject']}"

            name = cd['name']
            email = cd['email']
            phone = cd['phone']
            message = cd['message']

            msg = f"""
نام و نام خانوادگی: {name}
ایمیل فرستنده: {email}
شماره تماس: {phone or 'ثبت نشده'}

متن پیام:
{message}
"""

            email_message = EmailMessage(
                subject=subject,
                body=msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.EMAIL_HOST_USER],
                reply_to=[email]
            )

            email_message.send(fail_silently=False)

            sent = True
            form = ContactusForm()

    else:
        form = ContactusForm()

    return render(
        request,
        'blog/forms/contact-us.html',
        {
            'form': form,
            'sent': sent
        }
    )



def SharePost(request,post_id):
    post=get_object_or_404(Post,status='published',id=post_id)
    sent=False
    if request.method=='POST':
        form=ShareForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='دعوت کرده است{1} شما را به خواندن {0}'.format(cd['name'],post.title)
            message=cd['message']
            msg='{5}{4}{3}{2} در آدرس زیر دعوت کرده است {1} شما را به خواندن پست {0}'\
                .format(cd['name'],post.title,'\n',message,'\n',post_url)
            send_mail(subject, msg,'amin00karmi11@gmail.com',[cd['to']],fail_silently=False)
            sent=True
    else:
        form=ShareForm()
    return render(request,'blog/forms/share_post.html',{'form':form,'sent':sent,'post':post})


