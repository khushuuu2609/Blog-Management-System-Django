from django.contrib import admin
from blogmanageApp.models import Category, Post, Tag
from easy_select2 import select2_modelform, Select2Multiple

TagForm = select2_modelform(Post, attrs={'width': '250px'})

class TagAdmin(admin.ModelAdmin):
    form  = TagForm

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, TagAdmin)
