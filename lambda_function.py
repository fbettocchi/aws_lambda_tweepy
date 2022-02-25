
import logging
from os import environ
import tweepy

# tweepy is added to the layer on lambda using a local installation zipped eg:
# pip3 install tweepy -t lambda_python_tweety
# zip -r lambda_python_tweety.zip python

# dont forget to set the keys on your lambda ;)
API_KEY = environ['API_KEY']
API_SECRET_KEY = environ['API_SECRET_KEY']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def create_tweet():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    query = "1st query"
    query2 = "2nd query"
    reply = "your anwser #hashtag"

    tweets = api.search_tweets(query, lang='ISO_CODE', result_type='recent')
    tweets2 = api.search_tweets(query2, lang='ISO_CODE', result_type='recent')
    tweets.extend(tweets2)

    for tweet in tweets:
        # arbitrary, 3 to 5 is a good first indicator of trending tweet
        if tweet.favorite_count >= 3:
            status = api.get_status(tweet.id, tweet_mode="extended")
            if not status.favorited:
                # mark it as liked, since we have not done it yet, will avoid to interact again on it
                try:
                    tweet.favorite()
                except Exception as e:
                    logger.error("Error on fav", exc_info=True)
            if not status.retweeted:
                # Retweet and quote, since we have not retweeted it yet
                try:
                    tweet.retweet()
                    api.update_status(status=reply, in_reply_to_status_id=tweet.id,
                                      auto_populate_reply_metadata=True)

                except Exception as e:
                    logger.error("Error on fav and retweet", exc_info=True)


def lambda_handler(event, context):
    create_tweet()

    return {
        'statusCode': 200,
        'body': "done"
    }


# for local debug/dev
if __name__ == '__main__':
    create_tweet()
    
