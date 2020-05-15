from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from .models import ImageInfo
from PIL import Image

names = ["★조미형★ 생가", "션샤인랜드", "전라도음식이야기", "전주한옥마을", "전망카페",
         "더블유하우스 팬션", "덕인관", "메타프로방스", "삐에스몽테제빵소",
         "메타세콰이어가로수길", "담양관방제림", "미소댓잎국수", "죽녹원", "인기명"]

# Create your views here.
def index(request):

    spots = []
    for idx, name in enumerate(names):
        image_infos = []
        for info in ImageInfo.objects.filter(spot=idx).order_by('main'):
            image_infos.append(info)

        if len(image_infos) > 0:
            spots.append({'name': name, 'main': image_infos[0], 'image_infos': image_infos[1:]})
        else:
            spots.append({'name': name, 'main': None, 'image_infos': None})

    return render(request, 'memory/index.html', {'spots': spots})

def detail(request):
    spot = int(request.GET.get('spot'))
    images = ImageInfo.objects.filter(spot=spot).order_by('main')
    return render(request, 'memory/detail.html', {'spot': spot, "name": names[spot], "images": images})

def rotate_image(path, angle):
    print(path)
    img = Image.open(path)
    x = img.rotate(angle, expand=True)

    # crop the rotated image to the size of the original image
    #x = x.crop(box=(x.size[0] / 2 - img.size[0] / 2,
    #                x.size[1] / 2 - img.size[1] / 2,
    #                x.size[0] / 2 + img.size[0] / 2,
    #                x.size[1] / 2 + img.size[1] / 2))

    return x

def process_image(request):
    spot = int(request.GET.get('spot'))
    mode = request.GET.get('mode')
    id = int(request.GET.get('id'))
    if mode == "delete":
        image_info = ImageInfo.objects.filter(id=id)
        os.remove(image_info[0].image.path)
        image_info.delete()
    elif mode == "rotate":
        image_info = ImageInfo.objects.get(id=id)
        im = rotate_image(image_info.image.path, -90)
        im.save(image_info.image.path)
        image_info.revision = image_info.revision + 1
        image_info.save()
    elif mode == "reverse":
        image_info = ImageInfo.objects.get(id=id)
        im = rotate_image(image_info.image.path, 180)
        im.save(image_info.image.path)
        image_info.revision += 1
        image_info.save()
    elif mode == "main":
        image_info = ImageInfo.objects.filter(main=1)
        if len(image_info) > 0:
            image_info = ImageInfo.objects.get(id=image_info[0].id)
            image_info.main = False
            image_info.save()
        image_info = ImageInfo.objects.get(id=id)
        image_info.main = 1
        image_info.save()


    return redirect(f'/memory/detail?spot={spot}', {'spot': spot})

def upload(request):
    for image in request.FILES.getlist('image'):
        imageInfo = ImageInfo()
        imageInfo.spot = request.POST.get("spot", None)
        imageInfo.image = image
        imageInfo.revision = 0
        imageInfo.main = 0
        imageInfo.save()
    spots = {}
    return redirect('/memory', {'spots': spots})
