from django.db import models

class Directory(models.Model):
    path = models.CharField(max_length=255, unique=True)
    last_access_date = models.DateTimeField('last access', auto_now=True)
    
    def __str__(self):
        return self.path


class DirEntry(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    last_access_date = models.DateTimeField('last access', auto_now=True)
    in_progress = models.BooleanField(default=False)

    def __str__(self):
        return self.name
