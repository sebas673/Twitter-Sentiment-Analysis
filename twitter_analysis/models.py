from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .sentiment import sentiment
from django.contrib.postgres.fields import ArrayField
from django.core.validators import validate_comma_separated_integer_list
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

    # holds the tweets when we search by ids
    id_list = models.TextField(validators=[
        validate_comma_separated_integer_list], max_length=400, blank=True, verbose_name="Tweet IDs")
    old_id_list = models.CharField(validators=[
        validate_comma_separated_integer_list], max_length=200, blank=True)

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

        ids = self.id_list

        if ids:
            print("there are ids")
            print(type(ids))
        else:
            print("there are NO ids")
            print(ids)

        # print(len(s.split(',')))

        keywordTweetsRequested = 20
        timeTweetsRequested = 20

        # update keyword
        if self.old_keyword != self.keyword0 or not self.keyword0:
            keywordChanged = True
            self.old_keyword = self.keyword0
        else:
            keywordChanged = False

        # update id list
        if self.old_id_list != self.id_list:
            print("@@@@@@@@@@lists do not match")
            p = self.posIDs
            n = self.negIDs
            old_ids = self.old_id_list

            print("old ids:", old_ids)
            print("current ids:", self.id_list)

            if self.old_id_list:
                self.posIDs = [x for x in p if x not in old_ids]
                self.negIDs = [x for x in n if x not in old_ids]

            self.old_id_list = self.id_list

        # update the total number of tweets and keyword
        if keywordChanged or not self.id_list:
            oldTotal = 0
            oldNumPos = 0
            oldNumNeg = 0
            self.posID0 = 0
            self.negID0 = 0
            self.most_favorited = 0
            self.posIDs = []
            self.negIDs = []
            self.positive_percent0 = 0
            self.negative_percent0 = 0
            self.neutral_percent0 = 0
            self.times = []
            self.polarities = []
        else:
            oldTotal = self.total_num_tweets
            oldNumPos = self.total_num_pos
            oldNumNeg = self.total_num_neg

        # what type of search to do
        do_sentiment_analysis = True
        # keyword
        search = ""
        if self.keyword0 and not self.id_list:
            search = "keyword"
            print("kw and cleared the id list")
        # list
        elif not self.keyword0 and self.id_list:
            search = "id_list"
            print("list")
        # both
        elif self.keyword0 and self.id_list:
            search = "both"
            # print(self.id_list)
            print("both")

        # none
        else:
            do_sentiment_analysis = False
            print("NO search")

        # if the keyword is not empty
        if do_sentiment_analysis:
            print("do sentiment analysis")
            l = []
            if search == "id_list" or search == "both":
                l = self.id_list.split(',')
            # print(l)
            # print(len(l))
            keyword_results = sentiment(
                self.keyword0, keywordTweetsRequested, l, search)

            # update the total number of tweets
            numNewTweets = keyword_results[5]

            # no valid tweets were found
            # should we tell the user?
            if numNewTweets == 0:
                super().save(*args, **kwargs)
                return

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
            # if keywordChanged:
            #     listPos = []
            # else:
            listPos = self.posIDs

            if listPos is None:
                self.posIDs = keyword_results[0]
            else:
                listPos += keyword_results[0]
                mynewlist = list(set(listPos))
                print("len posids:", len(listPos))
                self.posIDs = mynewlist

            # add new negIDs to the list
            # if keywordChanged:
            #     listNeg = []
            # else:
            listNeg = self.negIDs

            if listNeg is None:
                self.negIDs = keyword_results[1]
            else:
                listNeg += keyword_results[1]
                mynewlist = list(set(listNeg))
                self.negIDs = mynewlist

            # update times for the line chart
            times_to_sort = []
            polarities_to_sort = []

            # if keywordChanged:
            #     newTimes = []
            # else:
            newTimes = self.times

            if newTimes is None:
                self.times = keyword_results[6]
            else:

                output = []
                seen = set()

                newTimes += keyword_results[6]

                for time in newTimes:
                    if time not in seen:
                        seen.add(time)
                        output.append(time)

                # self.times = output
                times_to_sort = output

            # update the polarities for the line chart
            # if keywordChanged:
            #     newPolarities = []
            # else:
            newPolarities = self.polarities

            if newPolarities is None:
                self.polarities = keyword_results[7]
            else:

                output = []
                seen = set()

                newPolarities += keyword_results[7]

                for polarity in newPolarities:
                    if polarity not in seen:
                        seen.add(polarity)
                        output.append(polarity)

                # self.polarities = output
                polarities_to_sort = output

            print("type time 2st:", type(times_to_sort[0]))
            print("type polarities 2st:", type(polarities_to_sort[0]))

            times_to_sort, polarities_to_sort = zip(
                *sorted(zip(times_to_sort, polarities_to_sort)))

            self.times = times_to_sort
            self.polarities = polarities_to_sort

        # save the updated campaign
        super().save(*args, **kwargs)
