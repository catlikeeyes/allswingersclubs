from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments.models import Comment


# extending generic Comments application for adding short comments
# unregister Comment model admin

try:
    admin.site.unregister(Comment)
except:
    pass

class ExtendedCommentsAdmin(CommentsAdmin):
	# new list_display with short_comment
    # Comment doesn't have short_comment, it adds in the directory.models
	list_display = ('name', 'ip_address', 'club_url', 'club_edit_url', 'submit_date', 'poster_url', 'comment', 'is_public', 'is_removed', )
	search_fields = ('comment', )

admin.site.register(Comment, ExtendedCommentsAdmin)