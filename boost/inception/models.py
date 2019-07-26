import io
from PIL import Image, ImageOps
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from bus_scrapy.settings import BOT_NAME, PARSER_NAME


class Images(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image.name

    @staticmethod
    def add_img_border(raw_img):
        img = Image.open(io.BytesIO(raw_img.read()))
        img = img.convert('RGB')
        img = ImageOps.expand(img, border=10, fill='red')
        output = io.BytesIO()
        img.save(output, format='jpeg')
        return InMemoryUploadedFile(output,
                                    'image', raw_img.name, 'image/jpeg', img.size, None)


class BusStation(models.Model):
    title = models.CharField(max_length=255)
    departure = models.DateTimeField()
    voyage = models.CharField(max_length=255)
    arrival = models.TimeField()
    cost = models.FloatField(null=True)
    status = models.CharField(max_length=255)
    place = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ('title', 'departure', 'voyage')

    def __str__(self):
        return f'{self.title}|{self.departure}|{self.voyage}'


class Scraper(models.Model):
    job_id = models.CharField(max_length=255, blank=True, default='')
    project_name = models.CharField(max_length=255, default=BOT_NAME)
    spider_name = models.CharField(max_length=255, default=PARSER_NAME)
    status = models.CharField(max_length=255, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.spider_name}-{self.job_id}'
