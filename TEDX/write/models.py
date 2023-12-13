from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from taggit.managers import TaggableManager 
#from ckeditor.fields import RichTextField 

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
 
    
       
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    Photo = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    tags = TaggableManager()
    
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name='Tposts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Uposts')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()
    
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('write:post_detail', 
                       args=[ self.publish.year, self.publish.month, self.publish.day, self.slug])
        
    #path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),   
        
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commentss')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentedd')
    body = models.TextField()
    image = models.ImageField(upload_to='comments/%Y/%m/%d/', blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        
    def __str__(self):
        return f'Comment by {self.author} on {self.post} '
    
