from django.contrib import admin

from .models import *

admin.site.register(MyUser)
admin.site.register(Message)
admin.site.register(Appeal)