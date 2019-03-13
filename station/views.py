from django.http import JsonResponse

from .models import Color, New


def color_list(request):
    _color_list = Color.objects.filter(sites__domain=request.get_host())
    color_dict = dict()
    for color in _color_list:
        color_dict[color.id] = color.name
    return JsonResponse(color_dict)


def new_list(request):
    _new_list = New.objects.filter(site__domain=request.get_host())
    new_dict = dict()
    for new in _new_list:
        new_dict[new.id] = new.title
    return JsonResponse(new_dict)
