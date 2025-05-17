from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def compress_image(image_field):
    image = Image.open(image_field)
    buffer = BytesIO()
    image.save(buffer, format="webp", quality=90)
    image_field.save("image.webp", ContentFile(buffer.getvalue()), save=False)
    return image_field
