from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


def create_watermark(image):
    """Обработка изображения путем наложения водяного знака.

    Передача исходного `image` и водяного изображения (из `avatars/watermark/watermark.png`)
    с последующим наложением в RGBA `paste()`.

    Далее изображение конвертируется из RGBA в RGB `convert()` и передается в поток `BytesIO()`
    для буфера байтов в памяти, где резервируется `save()` и возвращается для сохранения в базе данных.
    """
    pil_base_image = Image.open(image)
    pil_watermark = Image.open(r'avatars/watermark/watermark.png')
    pil_base_image.paste(pil_watermark, (0, 0), mask=pil_watermark)
    pil_base_image = pil_base_image.convert('RGB')
    new_image_io = BytesIO()
    pil_base_image.save(new_image_io, format='JPEG')
    return ContentFile(new_image_io.getvalue())
