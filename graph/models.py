from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField 
from imagekit.processors import ResizeToFill

# Create your models here.
class Graph(models.Model):
    def upload_path(self, filename):
        return 'user_files/{0}/Graphs/{1}'.format(self.user.username, filename)

    title = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to=upload_path, blank=True)
    created = models.DateTimeField(auto_now_add=True)
