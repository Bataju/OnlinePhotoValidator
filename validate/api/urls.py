from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import re_path


from . import views

def redirect_root(request):
    return HttpResponseRedirect('/photoValidator/')


urlpatterns = [
    path('photoValidator/', views.startPage, name='photoValidator'),
    path('upload/', views.process_image, name='upload'),
    path('dialogueBox/', views.dialogueBox, name='dialogueBox'),
    path('saveConfig/', views.save_config, name='save_config'),
    path('', redirect_root),
    path('image_gallery/', views.image_gallery, name='image_gallery'),
    # re_path(r'^image_gallery/$', views.image_gallery, name='image_gallery'),
    # path('image_gallery/<path:folder_path>/',views.image_gallery, name='image_gallery'),
]


