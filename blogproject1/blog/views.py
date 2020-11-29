from django.shortcuts import render,get_object_or_404
from blog.models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag
# Create your views here.
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render (request,'blog/post_list.html',{'post_list':post_list,'tag':tag})
from blog.forms import CommentsForm
def Post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentsForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentsForm()
    return render(request,'blog/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})
from django.core.mail import send_mail
from blog.forms import EmailSendForm
def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=="POST":
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absoulte_url())
            subject='{}({}) Recommends You To Read"{}"'.format(cd['name'],cd['email'],post.title)
            message='Read Post At:\n{} \n\n{} comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'bhuvankumar14g0104@gmail.com',[cd['to']])
            sent=True
    else:
        form=EmailSendForm()
    return render(request,'blog/sharebyemail.html',{'form':form,'post':post,'sent':sent})

