from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
#Tag
from taggit.managers import TaggableManager
# Create your models here.
class PostManager(models.Manager):
    def Y(self,year):
        return self.filter(publish__year=year)

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')
    
    
class Post(models.Model):
    STATUS_CHOICES=(
        ('draft','Draft'),
        ('published','Published'),
    )
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250,unique_for_date='publish')
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body=models.TextField() #TEXT
    publish=models.DateTimeField(default=timezone.now)
    Created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    test_field = models.CharField(max_length=10, default="hello")
    objects =PostManager()
    published=PublishedManager()
    tags=TaggableManager()
    class Meta:
        ordering=("-publish",)
        
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.slug,self.id])
        
        
    def __str__(self):
        return self.title

class Account(models.Model):
    GENDER_CHOICES=(
        ('آقا','آقا'),
        ('خانم','خانم'),
    )
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='account',)
    phone=models.CharField(max_length=11,null=True,blank=True)
    gender=models.CharField(max_length=5,choices=GENDER_CHOICES,default='آقا')
    address=models.TextField(null=True,blank=True)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    age=models.PositiveIntegerField(default=None,blank=True,null=True)
    
    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name
    
    

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    name=models.CharField(max_length=100)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=False)
    
    class Meta:
        ordering=('created',)
        
    def __str__(self):
        return f'نظر {self.name} درباره پست «{self.post.title}»'