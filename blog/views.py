from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Comment
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    blogs = Blog.objects.all().order_by('-id') #Blog 객체를 다 가져오겠다.
    return render(request, 'blog/home.html', {'blogs':blogs})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)

    user = request.user

    if blog_detail.likes.filter(id = user.id):
        message = "좋아요 취소"
    else:
        message = "좋아요"

    return render(request, 'blog/detail.html', {'blog':blog_detail, 'message':message})

def new(request): 
    return render(request, 'blog/new.html') #요청이 들어오면 이러한 파일을 보여줘라.

def create(request):
    blog = Blog() #붕어빵틀
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.user = get_object_or_404(User, pk=request.GET['user_id'])
    #붕어빵 틀 다 담았다.
    blog.save()

    return redirect('/blog/' + str(blog.id))

def edit(request,blog_id):
    blog= get_object_or_404(Blog, pk= blog_id) # 특정 객체 가져오기(없으면 404 에러)
    return render(request, 'blog/edit.html', {'blog':blog})

def update(request,blog_id):
    blog= get_object_or_404(Blog, pk= blog_id) # 특정 객체 가져오기(없으면 404 에러)
    blog.title = request.GET['title'] # 내용 채우기
    blog.body = request.GET['body'] # 내용 채우기
    blog.pub_date = timezone.datetime.now() # 내용 채우기
    blog.save() # 저장하기

    # 새로운 글 url 주소로 이동
    return redirect('/blog/' + str(blog.id))

def delete(request, blog_id):
    blog= get_object_or_404(Blog, pk= blog_id) # 특정 객체 가져오기(없으면 404 에러)
    blog.delete()
    return redirect('home') # home 이름의 url 로

def comment_create(request, blog_id):
    comment = Comment() #댓글을 저장하기 위해 빈 Comment 객체를 하나 생성
    comment.body = request.GET['content'] #댓글의 내용을 받아옴
    comment.blog = get_object_or_404(Blog, pk=blog_id) #해당 댓글을 어떤 blog 객체와 연결시켜 줄 것인지 찾아온다.
    comment.save() #comment를 db에 저장

    return redirect('/blog/'+str(blog_id))

def post_like(request, blog_id):
    user = request.user #로그인된 유저의 객체(정보)를 가져온다.
    blog = get_object_or_404(Blog, pk = blog_id) #좋아요 버튼을 누를 글을 가져온다.

    # 이미 좋아요를 눌렀다면 좋아요를 취소, 아직 안눌렀으면 좋아요를 누른다.
    if blog.likes.filter(id = user.id): #로그인한 user가 현재 blog 객체에 좋아요를 눌렀다면
        blog.likes.remove(user) #해당 좋아요를 없앤다
    else : #아직 좋아요를 누르지 않았다면
        blog.likes.add(user) #좋아요를 추가한다.

    return redirect('/blog/'+str(blog_id)) #좋아요 처리를 하고 detail 페이지로 간다.

