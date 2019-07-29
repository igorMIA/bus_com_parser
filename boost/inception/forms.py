from django.forms import ModelForm
from .models import Images


class ImageForm(ModelForm):
    """
    form for Image instance
    """
    class Meta:
        model = Images
        fields = '__all__'
