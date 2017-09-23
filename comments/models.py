from django.db import models


class Comment(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=300)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post')

    def _str_(self):
        return self.text[:20]
