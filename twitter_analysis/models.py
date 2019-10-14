from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# The Campaign Model is a user's virtual campaign
# A user can have many Campaigns, but each Campaign only has one owner


class Campaign(models.Model):

    # we'll need to add more fields eventually
    name = models.CharField(max_length=100)
    description = models.TextField()
    last_refreshed = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('campaign-detail', kwargs={'pk': self.pk})
