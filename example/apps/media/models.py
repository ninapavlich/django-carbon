from django.db import models
from django.conf import settings

from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from imagekit.models import ProcessedImageField
from imagekit.admin import AdminThumbnail
from imagekit.processors import ResizeToFill, ResizeToFit

from carbon.compounds.media.models import Image as BaseImage
from carbon.compounds.media.models import Media as BaseMedia
from carbon.compounds.media.models import SecureImage as BaseSecureImage
from carbon.compounds.media.models import SecureMedia as BaseSecureMedia

class Image(BaseImage):

    variants = ('thumbnail','width_1200', 'width_1200_fill', 'square_600')

    square_600 = ImageSpecField( source='image', format='PNG',
        processors=[ResizeToFill(600, 600)], options={'quality': 85})

    width_1200 = ImageSpecField( source='image', format='PNG',
        processors=[ResizeToFit(1200, None, False)], options={'quality': 85})

    width_1200_fill = ImageSpecField( source='image', format='PNG',
        processors=[ResizeToFit(1200, None)], options={'quality': 85})


class Media(BaseMedia):
    pass

class SecureImage(BaseSecureImage):

    variants = ('thumbnail','width_1200', 'width_1200_fill', 'square_600')

    square_600 = ImageSpecField( source='image', format='PNG',
        processors=[ResizeToFill(600, 600)], options={'quality': 85})

    width_1200 = ImageSpecField( source='image', format='PNG',
        processors=[ResizeToFit(1200, None, False)], options={'quality': 85})

    width_1200_fill = ImageSpecField( source='image', format='PNG',
        processors=[ResizeToFit(1200, None)], options={'quality': 85})


class SecureMedia(BaseSecureMedia):
    pass
