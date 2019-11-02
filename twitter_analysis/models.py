from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .sentiment import sentiment_by_keyword
# The Campaign Model is a user's virtual campaign
# A user can have many Campaigns, but each Campaign only has one owner


class Campaign(models.Model):

    # we'll need to add more fields eventually
    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.TextField(
        verbose_name="Notes")
    last_refreshed = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    keyword0 = models.CharField(
        max_length=50, default='', verbose_name="Keywords")
    positive_percent0 = models.IntegerField(default=0)
    negative_percent0 = models.IntegerField(default=0)
    neutral_percent0 = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('campaign-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        # resultsN[0] is positive, resultsN[1] is negative, resultsN[2] is neutral
        results0 = sentiment_by_keyword(self.keyword0)
        self.positive_percent0 = results0[0]
        self.negative_percent0 = results0[1]
        self.neutral_percent0 = results0[2]

        print("keyword: ", self.keyword0)
        print("positive: ", self.positive_percent0)
        print("negative: ", self.negative_percent0)
        print("neutral: ", self.neutral_percent0)
        print("total: ", self.positive_percent0 +
              self.negative_percent0 + self.neutral_percent0)

        super().save(*args, **kwargs)
