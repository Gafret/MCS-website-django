from django.db import models

from django.utils.timezone import now
from django.urls import reverse


from authentication.models import Profile

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=20)

class Article(models.Model):

    title = models.CharField(max_length=255 ,blank=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    # note that now is used without parenthesis that is because 
    # with them default value is set to the time models.py is run
    pub_date = models.DateField(default=now)  
    last_edit_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=False)

    text_body = models.TextField(verbose_name="text")
    sources = models.TextField(verbose_name="Sources", blank=True)
    sug_literature = models.TextField(verbose_name="Suggested Literature", blank=True)

    likes = models.ManyToManyField(Profile, related_name="liked_articles", blank=True)
    dislikes = models.ManyToManyField(Profile, related_name='disliked_articles', blank=True)
    bookmarks = models.ManyToManyField(Profile, related_name="bookmarked_articles", blank=True)
    
    tags = models.ManyToManyField(Tag, related_name='tagged_articles', blank=True)


    def get_absolute_url(self):
        return reverse('details', kwargs={"author":self.author, "slug":self.slug})
    

    # used to show only part of a text in html template
    def get_preview(self):
        preview = self.text_body.split()[:50]
        preview = ' '.join(preview) + "..."
        return preview


class Comment(models.Model):
    
    related_article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, related_name="my_comments", on_delete=models.CASCADE, null=True)

    comment_text = models.TextField()

    likes = models.ManyToManyField(Profile, related_name="liked_comments")
    dislikes = models.ManyToManyField(Profile)



