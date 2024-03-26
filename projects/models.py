from django.db import models
from django.urls import reverse
from django.shortcuts import get_object_or_404
from users.models import CustomUser


class Picture(models.Model):
    path = models.ImageField(upload_to='projects/images', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.path.url

    @property
    def show_url(self):
        return reverse('project.show', args=[self.id])
    
    @classmethod
    def get_project_by_id(cls, id):
        return get_object_or_404(cls, id=id)

class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(unique=True, max_length=100)
    details = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    total_target = models.FloatField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_projects')
    tags = models.ManyToManyField(Tag, blank=True ,related_name = 'projects')
    pictures = models.ManyToManyField(Picture, blank=True, related_name='projects')
    ratings = models.ManyToManyField(CustomUser, through='ProjectRating', related_name='project_ratings')
    reports = models.ManyToManyField(CustomUser , through='ProjectReport', related_name='project_reports')
    campaign_start_date = models.DateTimeField()
    campaign_end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def image_url(self):
        return f'{self.pictures.first()}'

class ProjectRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_ratings')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rated_projects')
    rating = models.IntegerField()

    def __str__(self):
        return self.rating

class Comment(models.Model):
    content = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authored_comments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    reports = models.ManyToManyField(CustomUser, through='CommentReport', related_name='comment_reports')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.content

class ProjectReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_reports')
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reported_projects')
    report_details = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class CommentReport(models.Model):
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reported_comments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reports')
    report_details = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)