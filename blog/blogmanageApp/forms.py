from django import forms
from blogmanageApp.models import Category
from blogmanageApp.models import Post, Tag
from easy_select2 import select2_modelform, Select2Multiple
from django_select2.forms import Select2MultipleWidget
from mptt.forms import TreeNodeChoiceField
from mptt.models import TreeManyToManyField


class PostForm(forms.ModelForm, forms.SelectMultiple):
    
    #tag = forms.ChoiceField(widget = Select2Widget() , initial= Tag)
    #Post form
    #Status fields make hidden and intial value is false
    #tag = ModelMultipleChoiceField(required=False, queryset=Contact.objects, widget=Select2MultipleWidget())
    status = forms.BooleanField( widget=forms.HiddenInput(), initial = False ,required= False)
    class Meta:
        model = Post
        fields = ['title','title_tag','tag','author','body','Category','status']
        widgets = {
                    'tag': Select2MultipleWidget
                }