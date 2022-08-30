# imports
import praw
import tweepy
import os
import urllib, urllib.request
import time
import random
from keys import keys  # api keys

# image save path
path = '/Users/dylan/PycharmProjects/TwitterBot/Images'


# check if a tweet has been previously posted
def posted_before(api, caption):
    statuses = api.user_timeline(count=200,include_rts=False,exclude_replies = True)
    for tweet in statuses:
        if caption == tweet.text:
            return True
    return False


def send_tweet(submission_title, file_path, file_name, reddit_username):
    # connect to API
    auth = tweepy.OAuth1UserHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # twitter caption
    tweet_text = submission_title + '\n\n' + 'Source: u/' + str(reddit_username) + ' on Reddit' + '\n' + '#dog #dogswithjobs'

    # make sure it hasn't been posted before
    if not posted_before(api, tweet_text):
        # upload the image
        file = open(file_path, 'rb')
        img = api.media_upload(filename = file_path, file=file)
        img_media_id = [img.media_id_string]

        # send tweet with caption and image
        api.update_status(status = tweet_text, media_ids = img_media_id)
        print("Tweet Sent!")
    else:
        print("Error: Submission has been previously tweeted")


def pull_subreddit_data():
    # create a reddit instance
    reddit = praw.Reddit(
        user_agent='Twitter Bot',
        client_id=keys['client_id'],
        client_secret=keys['client_secret'])

    # verify reddit connection
    if reddit.read_only:
        print("Connected to Reddit")

    # loop through top submission in r/DogsWithJobs
    for submission in reddit.subreddit('DogsWithJobs').top(limit=15, time_filter ='month'):

        file_name = submission.id
        url = submission.url
        reddit_username = submission.author

        # save image files and call send_tweet() function
        if url.endswith(".jpg") or url.endswith(".png") or url.endswith(".jpeg"):
            file_name += '.jpg'
            file_path = os.path.join(path, file_name)
            urllib.request.urlretrieve(url, file_path)
            # max submission title length of 200 characters
            send_tweet(submission.title[0:200], file_path, file_name, reddit_username)

        # tweet buffer
        sleep_time = random.randint(30,80)
        time.sleep(sleep_time)


pull_subreddit_data()
