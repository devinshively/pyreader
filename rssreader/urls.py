from django.conf.urls import patterns, url

from rssreader import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/results/
    url(r'^getFeeds/$', views.getFeeds, name='getFeeds'),
    # getArticlesForFeed
    url(r'^getArticlesForFeed/(?P<feedName>[A-Za-z].*)/$', views.getArticlesForFeed, name='getArticlesForFeed'),
    # toggleItemIsRead
    url(r'^toggleItemIsRead/(?P<articlePK>\d+)/$', views.toggleItemIsRead, name='toggleItemIsRead'),
    # search
    url(r'^searchArticles/(?P<searchCriteria>[A-Za-z].*)/$', views.searchArticles, name='searchArticles'),
    # getAllItemsInAllFeeds
    url(r'^getAllItemsInAllFeeds/$', views.getAllItemsInAllFeeds, name='getAllItemsInAllFeeds'),

    # getFavoriteArticles
    url(r'^getFavoriteArticles/$', views.getFavoriteArticles, name='getFavoriteArticles'),
    # toggleFavorite
    url(r'^toggleFavorite/(?P<articlePK>\d+)/$', views.toggleFavorite, name='toggleFavorite'),
    # deleteFeed
    url(r'^deleteFeed/(?P<feedUrl>[A-Za-z].*)/$', views.deleteFeed, name='deleteFeed'),
    # addFeed
    url(r'^addFeed/(?P<feedUrl>[A-Za-z].*)/$', views.addFeed, name='addFeed'),
)
