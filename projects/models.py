from django.db import models
from django.contrib.auth.models import User


class Picture(models.Model):
    path = models.ImageField(upload_to='projects/images', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # def __str__(self):
    #     return self.path

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete = models.CASCADE , related_name = 'categories')
    total_target = models.FloatField()
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'users')
    tags = models.ManyToManyField(Tag, related_name = 'tags')
    pictures = models.ManyToManyField(Picture, related_name = 'pictures')
    ratings = models.ManyToManyField(User, through= 'ProjectRating' , related_name='rated_projects')
    reports = models.ManyToManyField(User , through= 'ProjectReport', related_name='reported_projects')
    campaign_started_at = models.DateTimeField(auto_now=True)
    campaign_ended_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

class ProjectRating(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.IntegerField()

class Comment(models.Model):
    content = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete = models.CASCADE )
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    reports = models.ManyToManyField(User , through= 'CommentReport', related_name='reported_comments')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.content

class ProjectReport(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    reporter = models.ForeignKey(User, on_delete = models.CASCADE)
    report_details = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class CommentReport(models.Model):
    reporter = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    report_details = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)