from django.contrib import admin

from projects.models import Project,Category,Tag,Picture,Comment,ProjectRating,ProjectReport,CommentReport,Donations

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Picture)
admin.site.register(Comment)
admin.site.register(ProjectRating)
admin.site.register(ProjectReport)
admin.site.register(CommentReport)
admin.site.register(Donations)