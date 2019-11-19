from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .sentiment import sentiment_by_keyword, sentiment_by_time
from django.contrib.postgres.fields import ArrayField
# The Campaign Model is a user's virtual campaign
# A user can have many Campaigns, but each Campaign only has one owner


class Campaign(models.Model):

    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.TextField(verbose_name="Notes")
    last_refreshed = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    keyword0 = models.CharField(
        max_length=50, default='', verbose_name="Keywords")

    old_keyword = models.CharField(max_length=50, default='')

    positive_percent0 = models.IntegerField(default=0)
    negative_percent0 = models.IntegerField(default=0)
    neutral_percent0 = models.IntegerField(default=0)

    posID0 = models.CharField(max_length=70, default='')
    negID0 = models.CharField(max_length=70, default='')

    posIDs = ArrayField(models.CharField(
        max_length=100, default=''), null=True)
    negIDs = ArrayField(models.CharField(
        max_length=100, default=''), null=True)

    times = ArrayField(models.CharField(
        max_length=100, default=''), null=True)
    polarities = ArrayField(models.CharField(
        max_length=100, default=''), null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('campaign-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        # resultsN[0] is positive, resultsN[1] is negative, resultsN[2] is neutral
        numTweets = 30
        results0 = sentiment_by_keyword(self.keyword0, numTweets)
        self.positive_percent0 = results0[0]
        self.negative_percent0 = results0[1]
        self.neutral_percent0 = results0[2]

        if len(results0[3]) != 0:
            self.posID0 = results0[3][0]

        if len(results0[4]) != 0:
            self.negID0 = results0[4][0]

        # if the keyword has changed
        if self.old_keyword != self.keyword0:
            listPos = []
        else:
            # add new PositiveIDs to the ArrayField
            listPos = self.posIDs

        if listPos is None:
            self.posIDs = results0[3]

        else:
            listPos += results0[3]
            print("pos: ", listPos)
            self.posIDs = listPos

        if self.old_keyword != self.keyword0:
            listNeg = []
            self.old_keyword = self.keyword0
        else:
            listNeg = self.negIDs

        if listNeg is None:
            self.negIDs = results0[4]

        else:
            listNeg += results0[4]
            self.negIDs = listNeg

        results_time = sentiment_by_time(self.keyword0, numTweets)
        newTimes = self.times
        newTimes += results_time[0]
        self.times = newTimes

        newPolarities = self.polarities
        newPolarities += results_time[1]
        self.polarities = newPolarities

        super().save(*args, **kwargs)
