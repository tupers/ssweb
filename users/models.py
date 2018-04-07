# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    class Meta(AbstractUser.Meta):
        pass

class Order(models.Model):
    port = models.IntegerField()
    ip_group = models.IntegerField()
    strategy = models.IntegerField(default=0)
    owner = models.IntegerField()
    status = models.IntegerField(default=1)

    def __str__(self):
        brief = "id:%d, owner:%d, status:%d, port:%d, ip_group:%d"%(self.id,self.owner,self.status,self.port,self.ip_group)
        return brief
