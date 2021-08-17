from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='images/', null=True, blank=True)
    picture1 = models.ImageField(upload_to='images/', null=True, blank=True)
    picture2 = models.ImageField(upload_to='images/', null=True, blank=True)
    file = models.FileField(upload_to='files/')
    tex = models.TextField()
    code = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    key_comment = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comment_content')
    comment_text = models.TextField('')

    def __str__(self):
        return self.comment_text
