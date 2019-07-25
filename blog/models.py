from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model): # Blog라는 이름의 객체 틀을 만들겠다.
    title = models.CharField(max_length=200) #타이틀 이름으로 최대 200 글자의 데이터를 받겠다.
    pub_date = models.DateTimeField('date published') #pub_date라는 이름으로 시간 날짜 데이터를 받겠다.
    body = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, null='True')

    # m:n을 위한 속성
    likes = models.ManyToManyField(
        User, #USER 모델과 BLOG 모델을 M:N관계로 두겠다
        through = 'Like', #LIKE라는 중계 모델을 통해 M:N관계를 맺는다
        through_fields = ('blog','user'), # LIKE에 BLOG속성, USER속성을 추가하겠다
        related_name = 'likes'  #1:N 관계에서 BLOG에 연결된 COMMNET를 가져올 때 
        # COMMENT_SET으로 가져왔는데
        #RELATE_NAME을 설정하면 BLOG.LIKE_SET이 아니라
        #BLOG.LIKE로 BLOG와 관련된 LIKE를 가져올 수 있다.
    ) 
    # 이 객체를 가르키는 말을 title로 정하겠다
    def __str__(self):
        return self.title
    # 몇 개의 like와 연결되어 있는가를 보여준다.
    def like_count(self):
        return self.likes.count()
    
class Like(models.Model):
    #blog의 through_fields와 순서가 같아야 한다.
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, null = 'True')
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = 'True')

class Comment(models.Model):
    body = models.TextField()

    #Blog 모델과 관계를 맺어준다. 1:N에서 N의 속성으로 들어간다.
    # on_delete는 관계를 맺고 있는 Blog 객체가 삭제되면 관련된 Comment도 삭제시킨다.
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, null='True') 

    def __str__(self):
        return self.body
    