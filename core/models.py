import os
import uuid
from io import BytesIO

from PIL import Image as PilImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.translation import ugettext as _
from draceditor.models import DraceditorField

LANG_RU = 1
LANG_EN = 2
LANG_CHOICE = (
    (LANG_RU, 'Rus'),
    (LANG_EN, 'Eng'),
)


class Post(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name=_('Заголовок'))
    summary = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Общее'))
    body = DraceditorField(null=False, blank=False, verbose_name=_('История'))
    created_at = models.DateTimeField(null=False, blank=False, verbose_name=_('Создано в'))
    published_at = models.DateTimeField(null=False, blank=False, verbose_name=_('Опубликовано в'))
    uuid = models.UUIDField(null=True, blank=True, verbose_name=_('UUID'), unique=True)
    url_slug = models.CharField(max_length=150, null=False, blank=False, verbose_name='URL', unique=True)
    lang = models.PositiveSmallIntegerField(null=False, blank=False, default=LANG_RU, choices=LANG_CHOICE,
                                            verbose_name=_('Язык'))
    is_published = models.BooleanField(default=False, verbose_name=_('Опубликовано?'))
    is_page = models.BooleanField(default=False, verbose_name=_('Отдельная страница?'))
    head_image = models.ForeignKey('PostImage', to_field='id', db_column='head_image_id', null=True,
                                   blank=True,
                                   verbose_name=_('Картинка к посту'))

    @property
    def get_summary(self):
        return self.summary if self.summary else ''

    def __str__(self):
        return '{} {}'.format(self.title, self.published_at)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = str(uuid.uuid4())
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        db_table = 'posts'
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')
        ordering = ('-published_at',)


class PostImage(models.Model):
    origin = models.ImageField(null=False, blank=False, upload_to='p_img/%Y/%m/%d/')
    webp = models.ImageField(null=True, blank=True, upload_to='p_img/%Y/%m/%d/')
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True, verbose_name=_('Create date'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    def _to_webp(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.origin:
            return

        # Open original photo which we want to thumbnail using PIL's Image
        image = PilImage.open(BytesIO(self.origin.read()))
        image.thumbnail(image.size, PilImage.ANTIALIAS)

        # Save the thumbnail
        temp_handle = BytesIO()
        image.save(temp_handle, 'webp')
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into ImageField
        suf = SimpleUploadedFile(os.path.split(self.origin.name)[-1], temp_handle.read(), content_type='webp')
        # Save SimpleUploadedFile into image field
        self.webp.save(
            str(uuid.uuid4()) + '.webp',
            suf,
            save=False
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self._to_webp()
        return super(PostImage, self).save(*args, **kwargs)

    def __str__(self):
        if self.description:
            return self.description
        if self.created_at:
            return 'Img instance ({})'.format(self.created_at)
        return self.pk

    class Meta:
        db_table = 'images'
        verbose_name = _('Картинка к посту')
        verbose_name_plural = _('Картинки к постам')