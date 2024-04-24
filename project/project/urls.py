"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('guests',views.viewsets_guests)
router.register('movie',views.viewsets_movie)
router.register('reservation',views.viewsets_reservation)
urlpatterns = [
    path('admin/', admin.site.urls),
    #1
    path('django/jsonnomodel/',views.no_rest_no_model),
    #2
     path('django/jsonfrommodel/',views.no_rest_from_model),
    #3
    path('rest/fbv/',views.fbv_list),
     path('rest/fbv/<int:pk>',views.fdv_pk),
     #4
     path('rest/cbv/',views.cbv_list.as_view()),
    path('rest/cbv/<int:pk>',views.cbv_pk.as_view()),
    #5
    path('rest/mix/',views.mixing_list.as_view()),
     path('rest/mix/<int:pk>',views.mixing_pk.as_view()),
     #6
       path('rest/gin/',views.generics_list.as_view()),
     path('rest/gin/<int:pk>',views.generics_pk.as_view()),
     #7
    path('rest/viewsets/',include(router.urls)),
    #8
     path('findmovie/',views.find_movie),
     #9
       path('newreservation/',views.new_reservation),
    

    
]
