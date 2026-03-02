from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):   # fixed
        return self.name


class Nominee(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="nominee_images/", blank=True, null=True)
    votes = models.PositiveIntegerField(default=0)

    def _str_(self):   # fixed
        return f"{self.name} ({self.category.name})"
from django.contrib.auth.models import User

class UserVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nominee = models.ForeignKey(Nominee, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')  # one vote per category