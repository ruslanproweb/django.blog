from django.shortcuts import render, redirect
from .models import Article, Comment, Like, Dislike
from datetime import datetime
from .forms import LoginForm, RegistrationForm, CommentForm, ArticleForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DeleteView, ListView



def get_updated_time(queryset):
    current_time = datetime.now().timestamp()
    minutes_updated = [round((current_time - article.updated_at.timestamp()) / 60) for article in queryset]
    return list(map(lambda k, v: (k, v), queryset, minutes_updated))

class HomeView(ListView):
    model = Article
    template_name = 'core/index.html'
    context_object_name = 'articles'

    # def get_queryset(self):
    #     articles = super().get_queryset()
    #     return get_updated_time(articles)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        qs = get_updated_time(super().get_queryset())
        context['articles'] = qs
        return context





class SearchResults(HomeView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = super().get_queryset()
        filtered = qs.filter(title__iregex=query)
        print(filtered)
        return filtered

# DetailView


def home_view(request):
    articles = Article.objects.all()
    current_time = datetime.now().timestamp()
    minutes_updated = [round((current_time - article.updated_at.timestamp()) / 60) for article in articles]
    articles = list(map(lambda k, v: (k, v), articles, minutes_updated))
    context = {
        'articles': articles,
    }
    # отдать словарь в render
    return render(request, 'core/index.html', context)


def category_articles(request, category_id):
    articles = Article.objects.filter(category__id=category_id)
    current_time = datetime.now().timestamp()
    minutes_updated = [round((current_time - article.updated_at.timestamp()) / 60) for article in articles]
    articles = list(map(lambda k, v: (k, v), articles, minutes_updated))
    context = {
        'articles': articles,
    }
    # отдать словарь в render
    return render(request, 'core/index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)  # 1
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.article = article
            form.save()
            try:
                form.likes
            except Exception as e:
                Like.objects.create(comment=form)

            try:
                form.dislikes
            except Exception as e:
                Dislike.objects.create(comment=form)
            return redirect('article_detail', article.pk)
    else:
        form = CommentForm()

    try:
        article.likes
    except Exception as e:
        Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)

    comments = Comment.objects.filter(article=article)  # article_id
    total_comments_likes = {comment.pk: comment.likes.user.all().count() for comment in comments}
    total_comments_dislikes = {comment.pk: comment.dislikes.user.all().count() for comment in comments}
    total_likes = article.likes.user.all().count()
    total_dislikes = article.dislikes.user.all().count()
    context = {
        'article': article,
        'form': form,
        'comments': comments,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_comments_likes': total_comments_likes,
        'total_comments_dislikes': total_comments_dislikes
    }
    return render(request, 'core/detail.html', context)


def about_view(request):
    return render(request, 'core/about.html')


def contacts_view(request):
    return render(request, 'core/contacts.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

    else:  # GET запрос
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'core/login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:  # GET запрос
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'core/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def create_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)  # commit=False , не отправлять данные в БД
            form.author = request.user
            form.save()
            return redirect('article_detail', form.pk)
    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'core/article_form.html', context)


class UpdateArticleView(UpdateView):
    model = Article
    template_name = 'core/article_form.html'
    form_class = ArticleForm
    # success_url = '/'


class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'core/article_confirm_delete.html'
    success_url = '/'


# article/comment

def add_vote(request, obj_type, obj_id, action):
    from django.shortcuts import get_object_or_404

    obj = None
    if obj_type == 'article':
        obj = get_object_or_404(Article, pk=obj_id)
    elif obj_type == 'comment':
        obj = get_object_or_404(Comment, pk=obj_id)

    try:
        obj.likes
    except Exception as e:
        if obj.__class__ is Article:
            Like.objects.create(article=obj)
        else:
            Like.objects.create(comment=obj)

    try:
        obj.dislikes
    except Exception as e:
        if obj.__class__ is Article:
            Dislike.objects.create(article=obj)
        else:
            Dislike.objects.create(comment=obj)

    if action == 'add_like':
        if request.user in obj.likes.user.all():
            obj.likes.user.remove(request.user.pk)
        else:
            obj.likes.user.add(request.user.pk)
            obj.dislikes.user.remove(request.user.pk)
    elif action == 'add_dislike':
        if request.user in obj.dislikes.user.all():
            obj.dislikes.user.remove(request.user.pk)
        else:
            obj.dislikes.user.add(request.user.pk)
            obj.likes.user.remove(request.user.pk)
    # http://127.0.0.1:8000/articles/1
    return redirect(request.environ['HTTP_REFERER'])


def author_articles(request, username):
    user = request.user

    articles = Article.objects.filter(author=user)
    total_comments = sum([Comment.objects.filter(article=article).count() for article in articles])
    total_likes = sum([article.likes.user.all().count() for article in articles])
    print([article.likes.user.all().count() for article in articles])
    context = {
        'user': user,
        'total_articles': articles.count(),
        'total_comments': total_comments,
        'total_likes': total_likes,
        'articles': articles
    }
    return render(request, 'core/author_articles.html', context)