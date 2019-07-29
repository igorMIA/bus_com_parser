from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Images
from .forms import ImageForm
from .tasks import send_mail_task


def main_page(request):
    """
    view for main page
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'inception/index.html')


@login_required
def search_form(request):
    """
    view for search page
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'inception/search.html')


@login_required
def image_form(request):
    """
    view for image form
    send mail after success image uploading
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = Images.add_img_border(form.cleaned_data['image'])
            Images.objects.create(image=image)
            send_mail_task.delay(['content.manager@site.com'], 'Image was uploaded',
                                 'Image was added to our base, please verify')

    return render(request, 'inception/image_form.html', {'images': Images.objects.all()})
