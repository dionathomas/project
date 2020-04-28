from django.shortcuts import render
from django.http import JsonResponse
from sentiment.models import Tweet
from django.core import serializers
from main.models import Tutorial
from textblob import TextBlob
import tweepy
from .models import Tweet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string

# Create your views here.


emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
])

emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
])

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

emoticons = emoticons_happy.union(emoticons_sad)


def clean_tweets(tweet):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)

    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)

    tweet = emoji_pattern.sub(r'', tweet)

    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []

    for w in word_tokens:
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)


def dashboard(request):
    tut = Tutorial.objects.all()

    # Twitter credentials for the app
    consumer_key = '2v3ly3l0z8Ep1wAPSBmiTPiAG'
    consumer_secret = 'HqEqrIL0KbcoBmm58vP4ggnQxDjwTgrsQa8ejZAwX9R47eKDL6'
    access_key = '1056410205808816129-cEKUPOiK94hMHOPibbcLUpusS2185n'
    access_secret = 'nCd9XI3Fj36tszSGcAWDSCB4Rood103JsLX2aQK5CweRw'

    # pass twitter credentials to tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    for company in tut:

        if company.tutorial_has_twitter_data == False:

            companyname = str(company.tutorial_title)

            Tweets = tweepy.Cursor(api.search, q=companyname).items(50)

            for tweet in Tweets:
                print(companyname, '<-------------')
                print (tweet)
                analysis = TextBlob(tweet.text)
                subjectivity = analysis.sentiment.subjectivity
                polarity = analysis.sentiment.polarity
                tweet_text = tweet.text
                if polarity > 0:
                    tweet_sentiment = 'positive'
                elif polarity == 0:
                    tweet_sentiment = 'neutral'
                else:
                    tweet_sentiment = 'negative'

                tweet_obj = Tweet(customer_name=companyname, tweet_text=tweet_text, tweet_polarity=polarity,
                                  tweet_subjectivity=subjectivity, tweet_sentiment=tweet_sentiment)

                tweet_obj.save()

            company.tutorial_has_twitter_data = True
            company.save()

    return render(request, 'sentiment/sentiment.html', {"tutorials": Tutorial.objects.all})


def pivot_data(request):
    dataset = Tweet.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

