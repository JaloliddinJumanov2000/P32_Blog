from django.db import models

from config.settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model
User = get_user_model()

class Blog(models.Model):
    TYPES = {
        "Journal": 'Journal',
        "Life updates": "Life updates",
        "Travel": "Travel",
        "Personal development": "Personal development",
        "IT": "IT"
    }
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)  # lazy load
    title = models.CharField(max_length=200)
    content = models.TextField()
    photo = models.ImageField(upload_to='blog_images', blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPES, default="Journal")
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} {self.title}"


class Like(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f"{self.user.username}: {self.is_liked}"
        return f"Anonim: {self.is_liked}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"{self.user} - {self.message[:20]}"
