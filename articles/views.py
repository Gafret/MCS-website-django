from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.utils.text import slugify
from django.utils.timezone import now
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


from . import models

# Create your views here.

# refactor + add login constaint
def like_article(request):
    article_id = request.POST.get('like', False) or request.POST['dislike'] # if "like" in dict it doesn't check "dislike", if "dislike" in dict then gets article_id
    user = request.user
    article = models.Article.objects.get(pk=article_id)
    profile = user.profile

    if 'like' in request.POST:
        if profile in article.likes.all():     
            article.likes.remove(profile)
        else:
            article.likes.add(profile)
            article.dislikes.remove(profile)

    elif 'dislike' in request.POST:
        if profile in article.dislikes.all():     
            article.dislikes.remove(profile)
        else:
            article.dislikes.add(profile)
            article.likes.remove(profile)

    return HttpResponseRedirect(reverse('articles:home'))


def like_comment(request):
    comment_id = request.POST.get('like', False) or request.POST['dislike']
    user = request.user
    profile = user.profile
    comment = models.Comment.objects.get(pk=comment_id)
    slug = comment.related_article.slug

    if 'like' in request.POST:
        if profile in comment.likes.all():     
            comment.likes.remove(profile)
        else:
            comment.likes.add(profile)
            comment.dislikes.remove(profile)
            

    if 'dislike' in request.POST:
        if profile in comment.dislikes.all():     
            comment.dislikes.remove(profile)
        else:
            comment.dislikes.add(profile)
            comment.likes.remove(profile)

    return HttpResponseRedirect(reverse('articles:details', 
                                         kwargs={'author':profile, 
                                                 'slug':slug}))


def add_comment(request, author, slug):
    author_profile = author
    commenter_profile = request.user.profile
    related_article = models.Article.objects.get(author=author_profile, slug=slug)
    comment_text = request.POST['comment_text']

    comment = models.Comment.objects.create(author=commenter_profile, 
                                            related_article=related_article,    
                                            comment_text=comment_text)
    
    return HttpResponseRedirect(reverse('articles:details', 
                                         kwargs={'author':author_profile,
                                                 'slug':slug}))


class HomeView(ListView):
    model = models.Article
    template_name = 'articles/home_template.html'

    
class ArticleDetailsView(DetailView):
    model = models.Article
    template_name = 'articles/details_page.html'
    context_object_name = 'article'

    # takes arguments passed to the url and filters articles by their value
    def get_queryset(self):
        profile = self.kwargs['author']
        slug = self.kwargs['slug']

        return models.Article.objects.filter(slug=slug, author=profile)


class CreateArticleView(LoginRequiredMixin, CreateView):
    model = models.Article
    template_name = 'articles/create_article.html'
    fields = ['author', 'title', 'text_body', 'sources', 'sug_literature']

    # turns article title into a slug and assigns it to the slug field
    def form_valid(self, form):
        form.instance.slug = slugify(self.request.POST['title'])

        return super().form_valid(form)


class UpdateArticleView(UpdateView):
    model = models.Article
    template_name = 'articles/edit_article.html'
    fields = ['title', 'text_body', 'sources', 'sug_literature']

    # automatically sets last edit date for the article
    def form_valid(self, form):
        form.instance.last_edit_date = now()

        return super().form_valid(form)
    
    # default get_object method has to be overridden otherwise it doesn't behave 
    # properly while prepopulating form fields in editing view 
    def get_object(self):
        slug = self.kwargs['slug']
        profile = self.kwargs['author']

        return models.Article.objects.get(author=profile, slug=slug)
        

class DeleteArticleView(DeleteView):
    model = models.Article
    success_url = reverse_lazy('articles:home')


