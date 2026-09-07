from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField( max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateField(auto_now_add=True)    
    updated = models.DateField(auto_now=True)    
    status = models.CharField( max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    
    class Meta: #this meta will tell django,
                #how to handle Post Model
        ordering = ['-publish'] #tell django to desc items
        indexes = models.Index(fields = ['-publish']),
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        # return reverse("post_detail", kwargs={"pk": self.pk, "year": self.publish.year, "month": self.publish.month, "day": self.publish.day, "slug": self.slug})
        return reverse("post_detail", args=[ self.publish.year, self.publish.month, self.publish.day, self.slug])
    
class Comment(models.Model):
    post = models.ForeignKey( Post , on_delete=models.CASCADE, related_name = 'comments')
    name = models.CharField( max_length=80)
    email = models.EmailField(null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]
    def __str__(self):
        return f'Comment by {self.name} on{self.post}'
    