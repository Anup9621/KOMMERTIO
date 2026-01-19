from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    mobile_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.user_name
