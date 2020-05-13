from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ImageInfo

# Create your views here.
def index(request):
    names = ["★조미형★ 생가", "션샤인랜드", "전라도음식이야기", "전주한옥마을", "전망",
             "더블유하우스 팬션", "덕인관", "메타프로방스", "삐에스몽테제빵소",
             "메타세콰이어가로수길", "담양관방제림", "미소댓잎국수", "죽녹원", "인기명"]
    spots = []
    for idx, name in enumerate(names):
        image_infos = []
        for info in ImageInfo.objects.filter(spot=idx):
            image_infos.append(info)

        print(len(image_infos))
        if len(image_infos) > 0:
            spots.append({'name': name, 'main': image_infos[0], 'image_infos': image_infos[1:]})
        else:
            spots.append({'name': name, 'main': None, 'image_infos': None})

    return render(request, 'memory/index.html', {'spots': spots})

def upload(request):
    for image in request.FILES.getlist('image'):
        imageInfo = ImageInfo()
        imageInfo.spot = request.POST.get("spot", None)
        imageInfo.image = image
        imageInfo.save()
    spots = {}
    return redirect('/memory', {'spots': spots})