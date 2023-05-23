from django.db import models

# Create your models here.
class Editors(models.Model):
    editor_name = models.CharField(max_length = 200)
    num_users = models.IntegerField()
    def __str__(self):
        return f"{self.editor_name}-{self.num_users}"