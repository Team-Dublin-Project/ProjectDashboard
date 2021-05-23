from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class UserFile(models.Model):
    def upload_path(self, filename):
        return 'user_files/{0}/{1}'.format(self.user.username, filename)
    
    #data = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name='file_posted')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.TextField(null=True)
    file_loc = models.FileField(upload_to=upload_path, blank=True, null=True)
    content_type = models.CharField(max_length=10, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self, *args, **kwargs):
	    return self.name