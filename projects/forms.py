
from typing import Any
from django import forms
from projects.models import Project,Category,Tag,Picture,Comment, CommentReport, ProjectReport
from datetime import datetime

class CreateProjectModelForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    category = forms.ModelChoiceField(Category.objects,widget=forms.Select(attrs={'class': "form-control"}))
    tags = forms.ModelMultipleChoiceField(Tag.objects,widget=forms.SelectMultiple(attrs={'class': "form-control"}))
    details = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control","rows":"5"}))
    total_target = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control"}))
    campaign_start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': "form-control"}))
    campaign_end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': "form-control"}))

    class Meta:
        model= Project
        fields = ['title', 'category', 'tags', 'details', 'total_target','campaign_start_date','campaign_end_date']

    def clean_campaign_start_date(self):
        cleaned_data = super().clean()
        campaign_start_date = cleaned_data.get('campaign_start_date')
        if campaign_start_date and campaign_start_date < datetime.now().date():
            raise forms.ValidationError("campaign start date cannot be in the past.")
        return campaign_start_date
    
    def clean_campaign_end_date(self):
        cleaned_data = super().clean()
        campaign_end_date = cleaned_data.get('campaign_end_date')
        if campaign_end_date and campaign_end_date < datetime.now().date():
            raise forms.ValidationError("campaign end date cannot be in the past.")
        if campaign_end_date and campaign_end_date < cleaned_data.get('campaign_start_date'):
            raise forms.ValidationError("campaign end date should be after start date.")
        return campaign_end_date

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
    title = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    category = forms.ModelChoiceField(Category.objects,widget=forms.Select(attrs={'class': "form-control"}))
    tags = forms.ModelMultipleChoiceField(Tag.objects,widget=forms.SelectMultiple(attrs={'class': "form-control"}))
    details = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control","rows":"5"}))
    total_target = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control"}))
    campaign_start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': "form-control"}))
    campaign_end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class': "form-control"}))
    
    class Meta:
        model= Project
        fields = ['title', 'category', 'tags', 'details', 'total_target','campaign_start_date','campaign_end_date']

    def clean_campaign_start_date(self):
        cleaned_data = super().clean()
        campaign_start_date = cleaned_data.get('campaign_start_date')
        if campaign_start_date and campaign_start_date < datetime.now().date():
            raise forms.ValidationError("campaign start date cannot be in the past.")
        return campaign_start_date
    
    def clean_campaign_end_date(self):
        cleaned_data = super().clean()
        campaign_end_date = cleaned_data.get('campaign_end_date')
        if campaign_end_date and campaign_end_date < datetime.now().date():
            raise forms.ValidationError("campaign end date cannot be in the past.")
        if campaign_end_date and campaign_end_date < cleaned_data.get('campaign_start_date'):
            raise forms.ValidationError("campaign end date should be after start date.")
        return campaign_end_date
    
    # Override the save method to handle associated tags, category, and pictures
    def save(self, commit=True):
        project = super().save(commit=False)

        # Save associated tags
        project.tags.set(self.cleaned_data.get('tags'))
        
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

class NewCommentReportModelForm(forms.ModelForm):
    class Meta:
        model= CommentReport
        fields = ["report_details"]
    
    def save(self, commit=True, comment=None, reporter = None):
        report = super().save(commit=False)
        report.comment = comment
        report.reporter = reporter
        if commit:
            report.save()


class NewProjectReportModelForm(forms.ModelForm):
    class Meta:
        model= ProjectReport
        fields = ["report_details"]
    
    def save(self, commit=True, project=None, reporter = None):
        report = super().save(commit=False)
        report.project = project
        report.reporter = reporter
        if commit:
            report.save()