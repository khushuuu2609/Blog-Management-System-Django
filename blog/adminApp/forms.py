from django import forms
from blogmanageApp.models import Tag, Category

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag                
        fields = ('tag_name',)

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
