from django.db import models

class Report(models.Model):
    user = models.CharField(max_length=32)
    contact_method = models.CharField(max_length=32)
    contact_info = models.CharField(max_length=32)
    message = models.TextField()

    def __str__(self):
        return self.user
