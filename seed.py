import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from streamers.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.files.base import ContentFile
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random

def generate_posts():
    author = User.objects.first()
    if not author:
        author = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Создан пользователь 'admin'")

    Post.objects.all().delete()
    print("Старая база очищена.")

     streamers = [
        ("Bratishkinoff", "Король СНГ-стриминга...", "https://www.twitch.tv/bratishkinoff", ["СНГ", "Хайп", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/bratishkin.jpg.jpg"),
        ("Buster", "Легенда...", "https://www.twitch.tv/buster", ["СНГ", "Олдскул"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/buster.jpg.jpg"),
        ("StRoGo", "Ворвался в мировой топ-10...", "https://www.twitch.tv/strogo", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/Strogo.jpg.jpg"),
        ("Stariy_Bog", "Ночные стримы...", "https://www.twitch.tv/stariy_bog", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/stariy.jpg.webp"),
        ("m3wsu", "4к ELO в CS2...", "https://www.twitch.tv/m3wsu", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/m3wsu.jpg.jpg"),
        ("mokrivskyi", "Забрал сердца...", "https://www.twitch.tv/mokrivskyi", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/mokrivskyi.jpg.webp"),
        ("zxcursed", "Самый скандальный...", "https://www.twitch.tv/zxcursed", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/zxcursed.jpg.jpg"),
        ("Deko", "Главное лицо CS2...", "https://www.twitch.tv/deko", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/deko.jpg.jpg"),
        ("des0ut", "Утренний стример...", "https://www.twitch.tv/des0ut", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/des0ut.jpg.jpg"),
        ("Nix", "Голос Dota 2...", "https://www.twitch.tv/nix", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/Nix.jpg.jpg"),
        ("ALOHADANCE", "Король непредсказуемости...", "https://www.twitch.tv/alohadance", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/ALOHADANCE.jpg.jpg"),
        ("Iceberg", "Не боится говорить...", "https://www.twitch.tv/iceberg", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/iceberg.jpg.jpg"),
        ("RAMZES666", "Титулованный про-игрок...", "https://www.twitch.tv/ramzes666", ["СНГ", "Dota 2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/ramzes.jpg.jpg"),
        ("SilverName", "Легенда Hearthstone...", "https://www.twitch.tv/silvername", ["СНГ", "Hearthstone"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/silvername.jpg.jpg"),
        # Для PashaBiceps пока заглушка, так как на GitHub нет его фото
        ("PashaBiceps", "Поляк с сердцем...", "https://www.twitch.tv/pashabiceps", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/buster.jpg.jpg"),
        ("s1mple", "Величайший игрок...", "https://www.twitch.tv/s1mple", ["СНГ", "CS2"], "https://raw.githubusercontent.com/Inv1Ven/twitch-blog/main/static_avatars/S1mple.jpg.jpg"),
    ]

    print("Начинаем генерацию постов и аватарок...")
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

        # Генерация аватарки (кружок с буквой)
        try:
            img = Image.new('RGB', (200, 200), color=(random.randint(50, 150), random.randint(50, 150), random.randint(50, 150)))
            draw = ImageDraw.Draw(img)
            first_letter = title[0].upper()
            try:
                font = ImageFont.truetype("arial.ttf", 100)
            except:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), first_letter, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            draw.text(((200 - text_width) / 2, (200 - text_height) / 2 - 20), first_letter, fill="white", font=font)
            
            output = BytesIO()
            img.save(output, format='PNG')
            post.avatar.save(f"{slug}.png", ContentFile(output.getvalue()), save=True)
            print(f"[{count+1}/16] {title} добавлен.")
        except Exception as e:
            print(f"[{count+1}/16] Ошибка для {title}: {e}")

        count += 1

    print(f"Успешно добавлено {count} стримеров!")

if __name__ == '__main__':
    generate_posts()

    #http://127.0.0.1:8000/ #http://127.0.0.1:8000/admin/streamers/post/