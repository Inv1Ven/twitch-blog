import os
import django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from streamers.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta

def generate_posts():
    # Ищем автора (или создаем, если база пустая)
    author = User.objects.first()
    if not author:
        author = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Создан пользователь 'admin'")

    print("Начинаем генерацию постов...")

    streamers = [
        ("Bratishkinoff", "Король СНГ-стриминга...", "https://www.twitch.tv/bratishkinoff", ["СНГ", "Хайп", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/bratishkin.jpg"),
        ("Buster", "Легенда...", "https://www.twitch.tv/buster", ["СНГ", "Олдскул"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/buster.jpg"),
        ("StRoGo", "Ворвался в мировой топ-10...", "https://www.twitch.tv/strogo", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/Strogo.jpg"),
        ("Stariy_Bog", "Ночные стримы...", "https://www.twitch.tv/stariy_bog", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/stariy.jpg"),
        ("m3wsu", "4к ELO в CS2...", "https://www.twitch.tv/m3wsu", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/m3wsu.jpg"),
        ("mokrivskyi", "Забрал сердца...", "https://www.twitch.tv/mokrivskyi", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/mokrivskiy.jpg.jpg"),
        ("zxcursed", "Самый скандальный...", "https://www.twitch.tv/zxcursed", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/zxcursed.jpg"),
        ("Deko", "Главное лицо CS2...", "https://www.twitch.tv/deko", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/deko.jpg"),
        ("des0ut", "Утренний стример...", "https://www.twitch.tv/des0ut", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/des0ut.jpg"),
        ("Nix", "Голос Dota 2...", "https://www.twitch.tv/nix", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/Nix.jpg"),
        ("ALOHADANCE", "Король непредсказуемости...", "https://www.twitch.tv/alohadance", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/ALOHADANCE.jpg"),
        ("Iceberg", "Не боится говорить...", "https://www.twitch.tv/iceberg", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/iceberg.jpg"),
        ("RAMZES666", "Титулованный про-игрок...", "https://www.twitch.tv/ramzes666", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/ramzes.jpg"),
        ("SilverName", "Легенда Hearthstone...", "https://www.twitch.tv/silvername", ["СНГ", "Hearthstone"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/silvername.jpg"),
        ("PashaBiceps", "Поляк с сердцем...", "https://www.twitch.tv/pashabiceps", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/pashabiceps.jpg"), # <--- Теперь тут Паша
        ("s1mple", "Величайший игрок...", "https://www.twitch.tv/s1mple", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/S1mple.jpg"),
    ]

    count = 0

    for title, content, twitch_url, tags_list, avatar_url in streamers:
        if Post.objects.filter(title=title).exists():
            print(f"{title} уже существует, пропускаем.")
            count += 1
            continue

        slug = f"{slugify(title)}-{count}"
        
        post = Post.objects.create(
            title=title,
            slug=slug,
            content=content,
            author=author,
            status=Post.Status.PUBLISHED,
            twitch_url=twitch_url,
            avatar=avatar_url,
            publish=timezone.now() - timedelta(days=count)
        )
        post.tags.set(tags_list)
        print(f"{title} добавлен.")
        count += 1

    print(f"Готово! Обработано {count} стримеров.")

if __name__ == '__main__':
    generate_posts()

    #http://127.0.0.1:8000/ #http://127.0.0.1:8000/admin/streamers/post/