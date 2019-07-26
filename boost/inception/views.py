from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Images
from .forms import ImageForm
from .tasks import send_mail_task


def main_page(request):
    if request.method == 'GET':
        return render(request, 'inception/index.html')


def search_form(request):
    if request.method == 'GET':
        return render(request, 'inception/search.html')
#
#
# def country_form_post(request):
#     if request.method == 'POST':
#         form = CountryForm(request.POST)
#         form.save()
#
#         send_mail_task.delay(['content.manager@site.com'], 'Country was added',
#                              f'{form.cleaned_data["name"]} was added to our base, please verify')
#
#     return redirect(reverse('main_page'))
#
#
# def league_form(request):
#     context = {'countries': Country.objects.all()}
#     return render(request, 'inception/league_form.html', context)
#
#


def image_form(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = Images.add_img_border(form.cleaned_data['image'])
            Images.objects.create(image=image)

    return render(request, 'inception/image_form.html', {'images': Images.objects.all()})
