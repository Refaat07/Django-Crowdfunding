
from typing import Any
from django import forms
from projects.models import Project,Category,Tag,Picture,Comment

class CreateProjectModelForm(forms.ModelForm):
    campaign_start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    campaign_end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model= Project
        fields = ['title', 'details', 'category', 'total_target', 'tags','campaign_start_date','campaign_end_date']

    # Override the save method to handle associated tags, category, and pictures
    def save(self, commit=True,creator=None):
        project = super().save(commit=False)

        project.creator = creator

        # Save associated category
        category = self.cleaned_data.get('category')
        project.category = category

        # Save associated tags
        tags = self.cleaned_data.get('tags')
        project.save()

        for tag in tags:
            project.tags.add(tag)

        # Save associated images
        for picture in self.files.getlist('pictures'):
            project_picture = Picture.objects.create(path=picture)
            project.pictures.add(project_picture)

        if commit:
            project.save()

        return project


class EditProjectModelForm(forms.ModelForm):
    campaign_start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    campaign_end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    
    class Meta:
        model= Project
        fields = ['title', 'details', 'category', 'total_target', 'tags','campaign_start_date','campaign_end_date']

    # Override the save method to handle associated tags, category, and pictures
    def save(self, commit=True):
        project = super().save(commit=False)

        project.creator = self.instance.creator 

        # Save associated category
        category = self.cleaned_data.get('category')
        project.category = category

        # Retrieve tags from the instance
        instance_tags = self.instance.tags.all()  # Assuming 'tags' is a ManyToManyField


        new_tags = self.cleaned_data.get('tags')

        # Remove tags that are associated with the instance but not in the form submission
        for tag in instance_tags:
            if tag not in new_tags:
                project.tags.remove(tag)

        # Add new tags from the form submission
        for tag in new_tags:
            if tag not in instance_tags:
                project.tags.add(tag)

        # Save associated images
        for picture in self.files.getlist('pictures'):
            project_picture = Picture.objects.create(path=picture)
            project.pictures.add(project_picture)

        if commit:
            project.save()

        return project

class NewCommentModelForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ['content']
        
    def save(self, commit=True, user=None, project=None):
        comment = super().save(commit=False)
        comment.author = user
        comment.project = project

        if commit:
            comment.save()
