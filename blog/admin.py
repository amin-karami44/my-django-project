from django.contrib import admin
from .models import Post,Account,Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','publish','Created','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug':('title',)}
    rew_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('publish','status')
    list_editable = ('status',)
    list_display_links = ('slug',)
    

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('phone','user','age',)
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('name','body','post','created','active',)
    list_filter=('active','created','updated',)
    list_editable=('active',)