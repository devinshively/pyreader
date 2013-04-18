# Create your views here.
from django.http import HttpResponse
from django.core import serializers
from rssreader.models import Feed, Article
import feedparser
import datetime
import urllib

# https://www.instapaper.com/m?u={url}


def index(request):

    return HttpResponse('Welcome')


# List of feeds
def getFeeds(request):
    feeds = Feed.objects.all()
    data = serializers.serialize('json', feeds)
    return HttpResponse(data, mimetype='application/json')


# List of articles for given feed
def getArticlesForFeed(request, feedName):
    feedName = urllib.unquote(feedName)
    feed = Feed.objects.get(name=feedName)
    downloadArticlesForFeed(feed)
    articles = Article.objects.filter(feed=feed)
    data = serializers.serialize('json', articles)
    return HttpResponse(data, mimetype='application/json')


# List of all items in all feeds
def getAllItemsInAllFeeds(request):
    feeds = Feed.objects.all()
    for feed in feeds:
        downloadArticlesForFeed(feed)
    articles = Article.objects.all()
    data = serializers.serialize('json', articles)
    return HttpResponse(data, mimetype='application/json')


# Favorite items
def getFavoriteArticles(request):
    articles = Article.objects.filter(is_fav=True)
    data = serializers.serialize('json', articles)
    return HttpResponse(data, mimetype='application/json')


# Favorite toggle
def toggleFavorite(request, articlePK):
    article = Article.objects.get(pk=articlePK)
    article.is_fav = not article.is_fav
    article.save()
    return HttpResponse('Success')


# Search items
def searchArticles(request, searchCriteria):
    searchCriteria = urllib.unquote(searchCriteria)
    found = []
    articles = Article.objects.all()
    for article in articles:
        if searchCriteria in article.title or searchCriteria in article.content:
            found.append(article)

    data = serializers.serialize('json', found)
    return HttpResponse(data, mimetype='application/json')


# Read item / Unread item
def toggleItemIsRead(request, articlePK):
    article = Article.objects.get(pk=articlePK)
    article.is_read = not article.is_read
    article.save()
    return HttpResponse('Success')


# Delete feed
def deleteFeed(request, feedUrl):
    feedUrl = urllib.unquote(feedUrl)
    Feed.objects.get(url=feedUrl).delete()
    return HttpResponse('Success')


# Add feed
def addFeed(request, feedUrl):
    response = "Feed already exists"
    feedUrl = urllib.unquote(feedUrl)
    if not Feed.objects.filter(url=feedUrl).exists():
        feed = feedparser.parse(feedUrl)
        newFeed = Feed(name=feed.feed.title, url=feedUrl)
        newFeed.save()
        downloadArticlesForFeed(newFeed)
        response = "Success"

    return HttpResponse(response)


# Downloads latest articles for given feed
def downloadArticlesForFeed(feed):
    articles = feedparser.parse(feed.url)
    for article in articles.entries:
        title = ''
        link = ''
        description = ''
        published = ''

        if 'title' in article:
            title = article.get('title')
        if 'link' in article:
            link = article.get('link')
        if 'description' in article:
            description = article.get('description')
        if 'published' in article:
            published = article.get('published')
            try:
                published = datetime.datetime.strptime(published, '%a, %d %b %Y %H:%M:%S')
            except ValueError, v:
                if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                    published = published[:-(len(v.args[0])-26)]
                    published = datetime.datetime.strptime(published, '%a, %d %b %Y %H:%M:%S')
                else:
                    raise v

        if not published:
            published = datetime.datetime.now()

        # Check if article title is in list of articles for feed
        if not Article.objects.filter(feed=feed).filter(title=title).exists():
            newArticle = Article(title=title, content=description, date=published, feed=feed, url=link)
            newArticle.save()

