from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestPostsFeed(Feed):
    title = "Twitch Blog - Последние стримеры"
    link = "/rss/feed/"
    description = "Самые свежие профили стримеров на нашем блоге."

    def items(self):
        # Берем 5 последних опубликованных постов
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        # Короткое описание (первые 30 слов)
        return item.content[:100] + "..."

    def item_link(self, item):
        # Ссылка на полную страницу стримера
        return reverse('streamers:post_detail', args=[item.id])

    def item_pubdate(self, item):
        return item.publish