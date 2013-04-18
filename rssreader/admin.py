from django.contrib import admin
from rssreader.models import Feed, Article

class FeedAdmin(admin.ModelAdmin):
    fields = ['url', 'name']

admin.site.register(Feed, FeedAdmin)
admin.site.register(Article)
