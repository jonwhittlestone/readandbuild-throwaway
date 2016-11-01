from django.contrib import admin
# Register your models here.
from .models import Post



class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "timestamp", "updated"]
    list_display_links = ["title"]
    search_fields = ["title", "content"]

    exclude = ('slug',)
    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)