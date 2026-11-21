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
        ("Bratishkinoff", "Король СНГ-стриминга...", "https://www.twitch.tv/bratishkinoff", ["СНГ", "Хайп", "CS2"]),
        ("Buster", "Легенда, с которой начался движ...", "https://www.twitch.tv/buster", ["СНГ", "Олдскул"]),
        ("StRoGo", "Ворвался в мировой топ-10 Twitch...", "https://www.twitch.tv/strogo", ["СНГ", "CS2"]),
        ("Stariy_Bog", "Ночные стримы и культовый жест...", "https://www.twitch.tv/stariy_bog", ["СНГ", "Dota 2"]),
        ("m3wsu", "4к ELO в CS2...", "https://www.twitch.tv/m3wsu", ["СНГ", "CS2"]),
        ("mokrivskyi", "Забрал сердца миллионов...", "https://www.twitch.tv/mokrivskyi", ["СНГ", "CS2"]),
        ("zxcursed", "Самый скандальный стример СНГ...", "https://www.twitch.tv/zxcursed", ["СНГ", "Dota 2"]),
        ("Deko", "Главное лицо CS2 в СНГ...", "https://www.twitch.tv/deko", ["СНГ", "CS2"]),
        ("des0ut", "Утренний стример...", "https://www.twitch.tv/des0ut", ["СНГ", "CS2"]),
        ("Nix", "Голос Dota 2...", "https://www.twitch.tv/nix", ["СНГ", "Dota 2"]),
        ("ALOHADANCE", "Король непредсказуемости...", "https://www.twitch.tv/alohadance", ["СНГ", "Dota 2"]),
        ("Iceberg", "Не боится говорить то, что думает...", "https://www.twitch.tv/iceberg", ["СНГ", "Dota 2"]),
        ("RAMZES666", "Титулованный про-игрок...", "https://www.twitch.tv/ramzes666", ["СНГ", "Dota 2"]),
        ("SilverName", "Легенда Hearthstone в СНГ...", "https://www.twitch.tv/silvername", ["СНГ", "Hearthstone"]),
        ("PashaBiceps", "Поляк с сердцем СНГ-гиганта...", "https://www.twitch.tv/pashabiceps", ["СНГ", "CS2"]),
        ("s1mple", "Величайший игрок в истории CS:GO...", "https://www.twitch.tv/s1mple", ["СНГ", "CS2"]),
    ]

    print("Начинаем генерацию постов и аватарок...")
    count = 0

    for title, content, twitch_url, tags_list in streamers:
        slug = f"{slugify(title)}-{count}"
        
        post = Post.objects.create(
            title=title,
            slug=slug,
            content=content,
            author=author,
            status=Post.Status.PUBLISHED,
            twitch_url=twitch_url,
            publish=timezone.now() - timedelta(days=count)
        )
        post.tags.set(tags_list)

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