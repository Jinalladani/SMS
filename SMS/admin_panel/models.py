from django.db import models


class SettingModel(models.Model):
    key = models.CharField("Settings Key",max_length=255)
    value = models.CharField("Settings value",max_length=5000)