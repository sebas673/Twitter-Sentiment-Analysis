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

    def get_tweet_sentiment(self, tweet):
        '''
        word description [0], value [1]
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        polarity = analysis.sentiment.polarity

        # set polarities
        if polarity > 0:
            return 'positive', polarity
        elif polarity < 0:
            return 'negative', polarity
        else:
            return 'neutral', polarity

    def get_tweets(self, query, count, is_popular, searchType, ids):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        fetched_tweets = []

        try:

            # search from a keyword
            if searchType == "keyword":
                print("keyword search")
                if is_popular:
                    # call twitter api to fetch popular tweets
                    fetched_tweets = self.api.search(
                        q=query, count=count, tweet_mode='extended', result_type='popular')

                else:
                    # call twitter api to fetch recent tweets
                    fetched_tweets = self.api.search(
                        q=query, count=count, tweet_mode='extended', result_type='recent')

            # search from a list of tweet IDs
            elif searchType == "id_list":
                print("id list search")

                fetched_tweets = self.api.statuses_lookup(
                    ids, tweet_mode='extended')

            # do both
            elif searchType == "both":
                print("BOTH search")
                if is_popular:
                    # call twitter api to fetch popular tweets
                    fetched_tweets = self.api.search(
                        q=query, count=count, tweet_mode='extended', result_type='popular')

                else:
                    # call twitter api to fetch recent tweets
                    fetched_tweets = self.api.search(
                        q=query, count=count, tweet_mode='extended', result_type='recent')

                fetched_tweets += self.api.statuses_lookup(
                    ids, tweet_mode='extended')

            highest = 0
            highestID = ""

            print("num fetched tweets:", len(fetched_tweets))

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
                analysis = self.get_tweet_sentiment(tweet.full_text)
                parsed_tweet['sentiment'] = analysis[0]
                parsed_tweet['polarity'] = analysis[1]

                # save the tweet id
                parsed_tweet['id'] = tweet.id_str

                # save the time it was created at
                parsed_tweet['time'] = str(tweet.created_at)

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


def sentiment(string, numTweetsRequested, id_list, search):
    '''
    returns list of posIDs [0], negIDs [1], most favorited tweet [2], number of positive tweets [3],
    number of negative tweets [4], total number of tweets [5]. times [6], and polarities [7]
    '''

    print("insdie sentimenr")
    print("id list", id_list)
    print("search:", search)
    # creating object of TwitterClient Class
    api = TwitterClient()

    # calling function to get tweets
    tweets = api.get_tweets(
        query=string, count=numTweetsRequested, is_popular=True, searchType=search, ids=id_list)

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

    times = []
    polarities = []

    for tweet in tweets[0]:
        times.append(tweet['time'])
        polarities.append(tweet['polarity'])

    # print("type time 1st:", type(times[0]))
    # print("type polarities 1st:", type(polarities[0]))

    # print("num tweets requested:", numTweetsRequested)
    # print("num tweets returned:", len(tweets[0]))

    return pos_IDs, neg_IDs, tweets[1], len(ptweets), len(ntweets), len(tweets[0]), times, polarities


def main():

    keyword = "nick viall"
    count = 3

    # print("keyword: ", keyword)
    # print("number of tweets requested: ", count)
    # print()

    test = [985283781279043584,986019219107205120,985981907782397952,1089845796877594624,1145423817486958597,1170020887439040512,985211794720305152,1096205996232507392,986420848159576065,985232556386856963,985224231775432704,985264036437741568,1095626298754396170,1009953369799184384,988263656306675712,985663685900333057,985545006805991425,985960717978390531,1189714938484277248,1040570959026118661]

    results = sentiment(keyword, count, test, "id_list")

    # results_graph = sentiment_by_time(keyword, count)
    # print("times: ", results_graph[0])
    # print()
    # print("polarities: ", results_graph[1])

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
