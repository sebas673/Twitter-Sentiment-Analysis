import re
import os
import sys
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    '''
    Generic Twitter Class for polarities analysis.
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

    def get_tweet_sentiment(self, tweet, description):
        '''
        Utility function to classify polarities of passed tweet
        using textblob's polarities method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        polarity = analysis.sentiment.polarity

        if description:
            # set polarities
            if polarity > 0:
                return 'positive'
            elif polarity == 0:
                return 'neutral'
            else:
                return 'negative'

        else:
            return polarity

    def get_tweets(self, query, count, is_popular, description):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:

            if is_popular:
                # call twitter api to fetch popular tweets
                fetched_tweets = self.api.search(
                    q=query, count=count, tweet_mode='extended', result_type='popular')

            else:
                # call twitter api to fetch recent tweets
                fetched_tweets = self.api.search(
                    q=query, count=count, tweet_mode='extended', result_type='recent')

            highest = 0
            highestID = ""

            # parsing tweets one by one
            for tweet in fetched_tweets:

                if tweet.favorite_count > highest:
                    highest = tweet.favorite_count
                    highestID = tweet.id_str

                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.full_text

                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(
                    tweet.full_text, description)

                # save the tweet id
                parsed_tweet['id'] = tweet.id_str

                # save the time it was created at
                parsed_tweet['time'] = tweet.created_at

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets, highestID

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def sentiment_by_time(string, numTweetsRequested):
    '''a list of times and a list of corresponding polarities'''

    # creating object of TwitterClient Class
    api = TwitterClient()

    # calling function to get tweets
    tweets = api.get_tweets(query=string, count=numTweetsRequested,
                            is_popular=False, description=False)

    times = []
    polarities = []

    # add positive polarity and time to lists
    for tweet in tweets[0]:
        times.append(tweet['time'])
        polarities.append(tweet['sentiment'])

    times, polarities = zip(*sorted(zip(times, polarities)))

    return times, polarities


def sentiment_by_keyword(string, numTweetsRequested):
    '''
    returns list of posIDs [0], negIDs [1], most favorited tweet [2], number of positive tweets [3], 
    number of negative tweets [4], and total number of tweets [5]
    '''

    # creating object of TwitterClient Class
    api = TwitterClient()

    # calling function to get tweets
    tweets = api.get_tweets(query=string, count=numTweetsRequested,
                            is_popular=True, description=True)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets[0]
               if tweet['sentiment'] == 'positive']

    ntweets = [tweet for tweet in tweets[0]
               if tweet['sentiment'] == 'negative']

    pos_IDs = []
    neg_IDs = []

    for tweet in ptweets:
        pos_IDs.append(tweet['id'])

    for tweet in ntweets:
        neg_IDs.append(tweet['id'])

    return pos_IDs, neg_IDs, tweets[1], len(ptweets), len(ntweets), len(tweets[0])


def main():

    keyword = "trump"
    count = 3

    # print("keyword: ", keyword)
    # print("number of tweets requested: ", count)
    # print()

    # results = sentiment_by_keyword(keyword, count)

    results_graph = sentiment_by_time(keyword, count)
    print("times: ", results_graph[0])
    print()
    print("polarities: ", results_graph[1])

    # print()
    # print()
    # new_times, new_polarities = zip(
    #     *sorted(zip(results_graph[0], results_graph[1])))
    # print("new_times: ", new_times)
    # print()
    # print("new_polarities: ", new_polarities)


if __name__ == "__main__":
    # calling main function
    main()
