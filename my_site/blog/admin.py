from django.contrib import admin

from .models import Author, Tag, Post , Comment

admin.site.register(Tag)

admin.site.register(Author)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post_comment")


admin.site.register(Comment, CommentAdmin)


class PostAdmin (admin.ModelAdmin):
    list_filter = ('author', 'date', 'tags',)
    prepopulated_fields = {
        "slug" : ("title", "author",),
                           }

admin.site.register(Post, PostAdmin)

