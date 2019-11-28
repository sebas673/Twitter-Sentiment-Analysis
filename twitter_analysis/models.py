from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .sentiment import sentiment_by_keyword
from django.contrib.postgres.fields import ArrayField
from random import randint
# The Campaign Model is a user's virtual campaign
# A user can have many Campaigns, but each Campaign only has one owner


class Campaign(models.Model):

    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.TextField(verbose_name="Notes", blank=True)
    last_refreshed = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    keyword0 = models.CharField(
        max_length=50, default='', verbose_name="Keywords", blank=True)
    old_keyword = models.CharField(max_length=50, default='')
    id_list = models.TextField(verbose_name="Tweet IDs", blank=True)

    # polarity percentages
    positive_percent0 = models.IntegerField(default=0)
    negative_percent0 = models.IntegerField(default=0)
    neutral_percent0 = models.IntegerField(default=0)

    # the total number of tweets
    total_num_tweets = models.IntegerField(default=0)
    total_num_pos = models.IntegerField(default=0)
    total_num_neg = models.IntegerField(default=0)

    # pos, neg, and most favorited tweet on the dashboard
    posID0 = models.CharField(max_length=70, default='')
    negID0 = models.CharField(max_length=70, default='')
    most_favorited = models.CharField(max_length=70, default='')

    # list of tweetIDs as a string
    posIDs = ArrayField(models.CharField(
        max_length=70, default=''), null=True)
    negIDs = ArrayField(models.CharField(
        max_length=70, default=''), null=True)

    # times and polarities for the line chart
    times = ArrayField(models.CharField(
        max_length=100, default=''), null=True)
    polarities = ArrayField(models.CharField(
        max_length=100, default=''), null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('campaign-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        keywordTweetsRequested = 10
        timeTweetsRequested = 10

        if self.old_keyword != self.keyword0:
            keywordChanged = True
            self.old_keyword = self.keyword0
        else:
            keywordChanged = False

        # update the total number of tweets and keyword
        if keywordChanged:
            oldTotal = 0
            oldNumPos = 0
            oldNumNeg = 0
        else:
            oldTotal = self.total_num_tweets
            oldNumPos = self.total_num_pos
            oldNumNeg = self.total_num_neg

        # if the keyword is not empty
        if self.keyword0:
            keyword_results = sentiment_by_keyword(
                self.keyword0, keywordTweetsRequested)

            # update the total number of tweets
            numNewTweets = keyword_results[5]
            self.total_num_tweets = oldTotal + numNewTweets

            # update the number of positive tweets
            numNewPos = keyword_results[3]
            self.total_num_pos = oldNumPos + numNewPos

            # update the number of negative tweets
            numNewNeg = keyword_results[4]
            self.total_num_neg = oldNumNeg + numNewNeg

            # update the percentages
            posPercentage = round((oldNumPos + numNewPos) /
                                  (oldTotal + numNewTweets) * 100)
            self.positive_percent0 = posPercentage

            negPercentage = round((oldNumNeg + numNewNeg) /
                                  (oldTotal + numNewTweets) * 100)
            self.negative_percent0 = negPercentage

            self.neutral_percent0 = 100 - (posPercentage + negPercentage)

            # update the 3 dashboard tweets
            if len(keyword_results[0]) != 0:
                self.posID0 = keyword_results[0][randint(
                    0, len(keyword_results[0]) - 1)]

            if len(keyword_results[1]) != 0:
                self.negID0 = keyword_results[1][randint(
                    0, len(keyword_results[1]) - 1)]

            self.most_favorited = keyword_results[2]

            # add new posIDs to list
            if keywordChanged:
                listPos = []
            else:
                listPos = self.posIDs

            if listPos is None:
                self.posIDs = keyword_results[0]
            else:
                listPos += keyword_results[0]
                mynewlist = list(set(listPos))
                self.posIDs = mynewlist

            # add new negIDs to the list
            if keywordChanged:
                listNeg = []
            else:
                listNeg = self.negIDs

            if listNeg is None:
                self.negIDs = keyword_results[1]
            else:
                listNeg += keyword_results[1]
                mynewlist = list(set(listNeg))
                self.negIDs = mynewlist

            # results_time = sentiment_by_time(
            #     self.keyword0, timeTweetsRequested)

            # update times for the line chart
            if keywordChanged:
                newTimes = []
            else:
                newTimes = self.times

            if newTimes is None:
                self.times = keyword_results[6]
            else:
                newTimes += keyword_results[6]
                mynewlist = list(set(newTimes))
                self.times = mynewlist

            # update the polarities for the line chart
            if keywordChanged:
                newPolarities = []
            else:
                newPolarities = self.polarities

            if newPolarities is None:
                self.polarities = keyword_results[7]
            else:
                newPolarities += keyword_results[7]
                mynewlist = list(set(newPolarities))
                self.polarities = mynewlist

        # save the updated campaign
        super().save(*args, **kwargs)
