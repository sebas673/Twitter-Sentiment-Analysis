import re
import os
import sys
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = os.environ.get('consumer_key')
        consumer_secret = os.environ.get('consumer_secret')
        access_token = os.environ.get('access_token')
        access_token_secret = os.environ.get('access_token_secret')

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)

            # data = self.api.rate_limit_status()
            # print(data)

        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(
                q=query, count=count, tweet_mode='extended')

            # parsing tweets one by one
            for tweet in fetched_tweets:

                print("i")

                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.full_text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(
                    tweet.full_text)

                # save the tweet id
                parsed_tweet['id'] = tweet.id_str

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


# returns a tuple consisting of postive %, negative %, and neutral % (in that order)
def sentiment_by_keyword(string, numTweets):

    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query=string, count=numTweets)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    # percentage of positive tweets
    positivePercent = 100*len(ptweets)/len(tweets)
    # print("Positive tweets percentage: {} %".format(positivePercent))

    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    # percentage of negative tweets
    negativePercent = 100*len(ntweets)/len(tweets)
    # print("Negative tweets percentage: {} %".format(negativePercent))

    # percentage of neutral tweets
    neutralPercent = 100*(len(tweets) - len(ntweets) -
                          len(ptweets))/len(tweets)

    # print("Neutral tweets percentage: {} %".format(negativePercent))

    pos_IDs = []
    neg_IDs = []
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    print("num: ", len(ptweets))
    for tweet in ptweets[:2]:
        print(tweet['text'])
        print(tweet['id'])
        pos_IDs.append(tweet['id'])
        print("P")

        # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    print("num: ", len(ntweets))
    for tweet in ntweets[:2]:
        # print(tweet['text'])
        print(tweet['id'])
        neg_IDs.append(tweet['id'])
        print("N")

    return round(positivePercent), round(negativePercent), round(neutralPercent), pos_IDs, neg_IDs


def main():

    results = sentiment_by_keyword("trump", 10)
    print("positive: ", results[0])
    print("negative: ", results[1])
    print("neutral: ", results[2])
    print("total: ", results[0] + results[1] + results[2])


if __name__ == "__main__":
    # calling main function
    main()
