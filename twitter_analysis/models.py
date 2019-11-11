from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .sentiment import sentiment_by_keyword
from django.contrib.postgres.fields import ArrayField
# The Campaign Model is a user's virtual campaign
# A user can have many Campaigns, but each Campaign only has one owner


class Campaign(models.Model):

    # we'll need to add more fields eventually
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

        print("the new keyword is", self.keyword0)

        if len(results0[3]) != 0:
            self.posID0 = results0[3][0]

        if len(results0[4]) != 0:
            self.negID0 = results0[4][0]

        if self.old_keyword != self.keyword0:
            listPos = []
            print("pos not match")

        else:
            # add new PositiveIDs to the ArrayField
            listPos = self.posIDs

        # print(type(listPos))
        if listPos is None:
            print("&&&&&&&&&&")
            self.posIDs = results0[3]

        else:
            # print("listPost len before: ", len(listPos))
            # print("len additions: ", len(results0[3]))
            listPos += results0[3]
            # print("listPost len after: ", len(listPos))
            print("pos: ", listPos)
            self.posIDs = listPos

        if self.old_keyword != self.keyword0:
            listNeg = []
            self.old_keyword = self.keyword0
            print("neg not match and clear")

        else:
            # add new NegativeIDs to the ArrayField
            listNeg = self.negIDs

        # print(type(listNeg))
        if listNeg is None:
            print("##########")
            # print(results0[4])
            self.negIDs = results0[4]

        else:
            # print("listNeg len before: ", len(listNeg))
            # print("len additions: ", len(results0[4]))
            listNeg += results0[4]
            # print("listNeg len after: ", len(listNeg))
            print("negL ", listNeg)
            self.negIDs = listNeg

        # print("keyword: ", self.keyword0)
        # print("positive: ", self.positive_percent0)
        # print("negative: ", self.negative_percent0)
        # print("neutral: ", self.neutral_percent0)
        # print("total: ", self.positive_percent0 +
        #       self.negative_percent0 + self.neutral_percent0)

        super().save(*args, **kwargs)
