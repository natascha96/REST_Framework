from django.conf import settings
from django.db import models


class VokabelList(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Vokabel(models.Model):
    list = models.ForeignKey(VokabelList, related_name='vokabellists', on_delete=models.CASCADE)
    name1 = models.CharField(max_length=50)
    name2 = models.TextField(max_length=50)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.name1


class ListAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    list = models.ForeignKey(VokabelList, on_delete=models.CASCADE)
    role = models.CharField(max_length=5)

    def __str__(self):
        return self.user
