# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User
from .models import Order,Plan

# Register your models here.
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Plan)
