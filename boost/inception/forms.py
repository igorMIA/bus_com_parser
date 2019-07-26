from django.forms import ModelForm
from .models import Images


class ImageForm(ModelForm):
    class Meta:
        model = Images
        fields = '__all__'
