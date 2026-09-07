from django.contrib import admin
from django.db import models
from .models import Post, Comment
# Register your models here.
class AdminInterface(admin.ModelAdmin):
    list_display = [
        'title',
        'slug',
        'author',
        'publish',
        'status',
    ]
    search_fields = [
        'title',
        'body',
    ]
    list_filter = ['status', 'created', 'publish', 'author']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS
admin.site.register(Post, AdminInterface)

class CommentModel(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'post', 
        'created',
        'active'
    ]
    list_filter = [
        'active',
        'created',
        'updated'
    ]
    search_fields = [
        'name',
        'email',
        'body'
    ]
admin.site.register(Comment, CommentModel)

