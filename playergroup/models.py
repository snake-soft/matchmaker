from django.db import models
from django.contrib.auth.models import Group


class Playergroup(models.Model):
    playergroups = models.ManyToManyField(Group)
