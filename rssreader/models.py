from django.db import models

# Create your models here.
class Feed(models.Model):
    url = models.TextField()
    name = models.TextField()

    # Description
    def __unicode__(self):
        return self.name


class Article(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.TextField()
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    is_fav = models.BooleanField(default=False)
    date = models.DateTimeField('date published')
    url = models.TextField()


    # Description
    def __unicode__(self):
        return self.title
