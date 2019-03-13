from django.urls import path

from .views import color_list, new_list

urlpatterns = [
    path('color-list', color_list, name='color-list'),
    path('new-list', new_list, name='new-list'),
]
