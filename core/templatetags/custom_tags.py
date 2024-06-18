from django.template import Library

from core.models import Category, Article, Comment


register = Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def is_category_current(request, category_id):
    return str(category_id) in request.path


@register.simple_tag()
def is_vote_exists(request, obj, vote_type):
    user = request.user

    if isinstance(obj, Article) and vote_type == 'likes':
        return user in obj.likes.user.all()
    elif isinstance(obj, Article) and vote_type == 'dislikes':
        return user in obj.dislikes.user.all()
    elif isinstance(obj, Comment) and vote_type == 'likes':
        return user in obj.likes.user.all()
    elif isinstance(obj, Comment) and vote_type == 'dislikes':
        return user in obj.dislikes.user.all()



